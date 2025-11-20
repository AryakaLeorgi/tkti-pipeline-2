pipeline {
    agent any

    environment {
        GROQ_API_KEY = credentials('groq-api-key')   // simpan di Jenkins Credentials
    }

    stages {

        stage('Setup Python venv') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install --upgrade pip
                pip install pandas scikit-learn joblib requests
                '''
            }
        }

        stage('Train ML Model') {
            steps {
                sh '''
                . .venv/bin/activate
                python3 ml/train_model.py
                '''
            }
        }

        stage('Simulate Pipeline Execution') {
            steps {
                script {
                    // error text collector
                    env.PIPELINE_ERROR = ""

                    // --- BUILD ---
                    def buildOutput = sh(script: "python3 ml/failure_simulation.py build", returnStdout: true)
                    echo buildOutput
                    if (buildOutput.contains("[FAILED]")) {
                        env.PIPELINE_ERROR += "\\nBUILD ERROR DETECTED"
                    }

                    // --- TEST ---
                    def testOutput = sh(script: "python3 ml/failure_simulation.py test", returnStdout: true)
                    echo testOutput
                    if (testOutput.contains("[FAILED]")) {
                        env.PIPELINE_ERROR += "\\nTEST ERROR DETECTED"
                    }

                    // --- DEPLOY ---
                    def deployOutput = sh(script: "python3 ml/failure_simulation.py deploy", returnStdout: true)
                    echo deployOutput
                    if (deployOutput.contains("[FAILED]")) {
                        env.PIPELINE_ERROR += "\\nDEPLOY ERROR DETECTED"
                    }

                    if (env.PIPELINE_ERROR == "") {
                        env.PIPELINE_ERROR = "NO ERRORS"
                    }

                    echo "Pipeline Error Summary: ${env.PIPELINE_ERROR}"
                }
            }
        }

        stage('Run Anomaly Detection') {
            steps {
                sh '''
                . .venv/bin/activate
                python3 ml/detect_anomaly.py
                '''
            }
        }

        stage('AI Auto Fix (Groq)') {
            when {
                expression { return env.PIPELINE_ERROR != "NO ERRORS" }
            }
            steps {
                sh '''
                . .venv/bin/activate
                export GROQ_API_KEY=$GROQ_API_KEY

                echo "=== Sending Error to Groq AI ==="
                python3 ml/auto_fix_code.py "$PIPELINE_ERROR" > ai_fix_output.txt
                '''
                echo "===== AI FIX SUGGESTION ====="
                echo readFile("ai_fix_output.txt")
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}
