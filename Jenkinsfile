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
                    pip install pandas scikit-learn joblib requests
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

                    echo result
                    env.ANOMALY_DETECTED = result.contains("ANOMALY_FLAG=true") ? "true" : "false"
                }
            }
        }
    }

    post {
        failure {
            // Jika pipeline gagal di tahap manapun: otomatis dijelaskan oleh AI
            explainError(
                // optional: batasi analisa log
                maxLines: 300,
                logPattern: '(?i)(error|failed|exception)'
            )
        }
        always {
            echo "Pipeline finished."
        }
    }
}
