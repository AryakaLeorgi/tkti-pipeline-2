pipeline {
    agent any

    environment {
        METRICS_FILE = 'pipeline_metrics.csv'
        MODEL_FILE = 'pipeline_success_model.pkl'
    }

    stages {
        stage('Simulate Metrics') {
            steps {
                echo "Generating or using existing metrics..."
                // Your previous simulation step or just reuse old file
            }
        }

        stage('AI Predict Success') {
            steps {
                script {
                    // Example simulated data (you could compute or read from CSV)
                    def buildTime = 3.5
                    def testTime = 1.8
                    def deployTime = 0.9
                    def failureReason = "None"

                    echo "🤖 Running ML prediction..."
                    sh """
                        python3 predict_pipeline.py \
                        --buildTime=${buildTime} \
                        --testTime=${testTime} \
                        --deployTime=${deployTime} \
                        --failureReason=${failureReason}
                    """
                }
            }
        }

        stage('Conditional Execution') {
            when {
                expression {
                    // Optionally skip this stage if previous prediction failed
                    // (Exit code from predict_pipeline.py can be used to fail/pause pipeline)
                    true
                }
            }
            steps {
                echo "🚀 Proceeding with build/test/deploy since prediction passed."
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*.csv,*.pkl', fingerprint: true
            echo "📊 Metrics & model archived."
        }
    }
}
