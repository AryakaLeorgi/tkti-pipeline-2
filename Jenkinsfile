pipeline {
    agent any

    stages {
        stage('Simulate Metrics') {
            steps {
                echo "Generating or using existing metrics..."
            }
        }

        stage('AI Predict Success') {
            steps {
                echo "🤖 Running ML prediction..."
                script {
                    def output = sh(
                        script: "python3 predict_pipeline.py --buildTime=3.5 --testTime=1.8 --deployTime=0.9 --failureReason=None",
                        returnStdout: true
                    ).trim()

                    echo "🔍 Model Output:\n${output}"

                    // Extract numeric prediction (0 or 1)
                    def match = (output =~ /Prediction result: (\d)/)
                    def prediction = match ? match[0][1].toInteger() : -1

                    if (prediction == 1) {
                        echo "✅ ML predicts SUCCESS — continuing pipeline..."
                    } else {
                        echo "🛑 ML predicts FAILURE — aborting pipeline!"
                        error("Aborted by ML prediction")
                    }
                }
            }
        }

        stage('Conditional Execution') {
            when {
                expression {
                    // Only run if previous stage didn't fail
                    currentBuild.resultIsBetterOrEqualTo("SUCCESS")
                }
            }
            steps {
                echo "🚀 Proceeding with build/test/deploy since prediction passed."
            }
        }
    }

    post {
        always {
            echo "📦 Archiving ML artifacts..."
            archiveArtifacts artifacts: 'pipeline_success_model4.pkl, model_columns.pkl, model_metrics.json, feature_importance.png, prediction_output.txt', fingerprint: true
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed due to ML prediction or other error."
        }
    }
}
