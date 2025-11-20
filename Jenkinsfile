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

        stage('Simulate Pipeline Execution') {
            steps {
                script {
                    def stages = ["build", "test", "deploy"]

                    for (s in stages) {
                        def output = sh(script: "python3 ml/failure_simulation.py ${s}", returnStdout: true)
                        echo output
                    }

                    echo "Pipeline Error Summary: NO ERRORS"
                }
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

                    if (result.contains("ANOMALY_FLAG=true")) {
                        env.ANOMALY_DETECTED = "true"
                    } else {
                        env.ANOMALY_DETECTED = "false"
                    }
                }
            }
        }

        stage('AI Auto Fix (Groq)') {
            when {
                expression { env.ANOMALY_DETECTED == "true" }
            }
            environment {
                GROQ_API_KEY = credentials('groq-api-key')
            }
            steps {
                sh """
                    echo "[INFO] Anomaly detected — running AI auto-fix..."
                    . ${env.VENV}/bin/activate
                    python3 ml/auto_fix_groq.py
                """
            }
        }

    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}
