pipeline {
    agent any

    environment {
        PYTHON = "python3"
        VENV = ".venv"
    }

    stages {

        stage('Setup Python venv') {
            steps {
                sh """
                    ${env.PYTHON} -m venv ${env.VENV}
                    . ${env.VENV}/bin/activate
                    pip install --upgrade pip
                    pip install pandas scikit-learn joblib numpy requests
                """
            }
        }

        stage('Generate Synthetic Dataset') {
            steps {
                sh """
                    . ${env.VENV}/bin/activate
                    python3 generate_pipeline_dataset.py
                """
            }
        }

        stage('Inject Anomaly Cases') {
            steps {
                sh """
                    . ${env.VENV}/bin/activate
                    python3 ci/simulate_error.py || true
                """
            }
        }

        stage('Train ML Model') {
            steps {
                sh """
                    . ${env.VENV}/bin/activate
                    python3 ml/train_model.py
                """
            }
        }

        stage('Run Anomaly Detection') {
            steps {
                script {
                    def result = sh(
                        script: ". ${env.VENV}/bin/activate && python3 ml/detect_anomaly.py",
                        returnStdout: true
                    ).trim()

                    echo "=== ANOMALY DETECTOR OUTPUT ==="
                    echo result
                    echo "================================"

                    if (result.contains("ANOMALY_FLAG=true")) {
                        echo "⚠ Detected potential anomaly!"
                        env.ANOMALY_DETECTED = "true"
                    } else {
                        env.ANOMALY_DETECTED = "false"
                    }
                }
            }
        }

        stage('AI Root Cause Analysis') {
            when {
                expression { return env.ANOMALY_DETECTED == "true" }
            }
            steps {
                sh """
                    . ${env.VENV}/bin/activate
                    python3 ml/ai_root_cause.py > ml_report.txt
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
            archiveArtifacts artifacts: 'ml_report.txt', allowEmptyArchive: true
        }
    }
}
