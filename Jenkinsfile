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

                    // Run anomaly detection
                    def result = sh(
                        script: ". ${env.VENV}/bin/activate && python3 ml/detect_anomaly.py",
                        returnStdout: true
                    ).trim()

                    echo result

                    // List alasan error random
                    def randomErrors = [
                        "Data pipeline mengalami lonjakan nilai yang tidak biasa.",
                        "Model mendeteksi nilai outlier pada fitur 'CPU Load'.",
                        "Distribusi data terbaru tidak cocok dengan pola historis.",
                        "Terdapat missing values yang melonjak signifikan.",
                        "Perubahan drastis pada variance dataset terdeteksi.",
                        "Data terbaru memiliki korelasi abnormal antar-fitur.",
                        "Anomaly disebabkan oleh input data yang tidak stabil.",
                        "Fitur 'response_time' naik jauh di atas batas wajar.",
                        "Terjadi ketidaksesuaian antara schema data dan model.",
                        "Model confidence terlalu rendah untuk data kali ini."
                    ]

                    // Pilih random reason
                    def reason = randomErrors[new Random().nextInt(randomErrors.size())]

                    if (result.contains("ANOMALY_FLAG=true")) {

                        echo "[ERROR] Anomaly detected!"
                        echo "[ERROR] Possible cause: ${reason}"

                        // Trigger Explain Error plugin
                        error("Anomaly detected — failing pipeline to trigger Explain Error plugin.")
                    }
                }
            }
        }

    }

    post {
        failure {
            explainError(
                maxLines: 200,
                logPattern: '(?i)(error|failed|exception|traceback)'
            )
        }
        always {
            echo "Pipeline finished."
        }
    }
}
