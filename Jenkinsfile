pipeline {
    agent any

    stages {

        stage('Setup Environment') {
            steps {
                echo "🔧 Creating virtual environment..."
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Simulation Build') {
            steps {
                echo "🚀 Running CI/CD simulation..."
                sh """
                    . venv/bin/activate
                    python simulation/run_simulation.py --output pipeline_metrics.csv
                """
                echo "✅ Simulation complete."
            }
        }

        stage('Train ML Model') {
            steps {
                echo "📚 Training Machine Learning model..."
                sh """
                    . venv/bin/activate
                    python ml/train_model.py
                """
            }
        }

        stage('Evaluate with ML') {
            steps {
                echo "🤖 Evaluating pipeline with ML..."
                sh """
                    . venv/bin/activate
                    python ml/evaluate_pipeline.py
                """
            }
        }

        stage('ML Feedback Loop') {
            steps {
                echo "🔁 Running ML feedback loop optimizer..."
                sh """
                    . venv/bin/activate
                    python ml/optimize_pipeline.py
                """
            }
        }

        stage('Show Optimization Report') {
            steps {
                echo "📘 Optimization Summary:"
                script {
                    def report = readFile "optimization_report.txt"
                    echo report
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'pipeline_metrics.csv'
                archiveArtifacts artifacts: 'ml/model.pkl'
                archiveArtifacts artifacts: 'optimization_report.txt'
                echo "📦 Artifacts saved."
            }
        }

    }

    post {
        success {
            echo "🎉 Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
