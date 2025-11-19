pipeline {
    agent any

    environment {
        PYENV = ".venv"
    }

    stages {

        stage('Setup Python Env') {
            steps {
                sh """
                    python3 -m venv ${PYENV}
                    . ${PYENV}/bin/activate
                    pip install --break-system-packages -r requirements.txt
                """
            }
        }

        stage('Build') {
            steps {
                script {
                    echo "Running build..."
                    sh "python3 ml/failure_simulation.py build > build.log"
                    build_time = sh(script: "grep 'DURATION:' build.log | awk '{print \$2}'", returnStdout: true).trim()
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "Running tests..."
                    sh "python3 ml/failure_simulation.py test > test.log"
                    test_time = sh(script: "grep 'DURATION:' test.log | awk '{print \$2}'", returnStdout: true).trim()
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Deploying..."
                    sh "python3 ml/failure_simulation.py deploy > deploy.log"
                    deploy_time = sh(script: "grep 'DURATION:' deploy.log | awk '{print \$2}'", returnStdout: true).trim()
                }
            }
        }

        stage('Log Real Metrics') {
            steps {
                sh """
                    . ${PYENV}/bin/activate
                    python3 ml/log_real_metrics.py \
                        --build ${build_time} \
                        --test ${test_time} \
                        --deploy ${deploy_time}
                """
            }
        }

        stage('Train ML Model') {
            steps {
                sh """
                    . ${PYENV}/bin/activate
                    python3 ml/train_model.py
                """
            }
        }

        stage('Predict Optimal Durations') {
            steps {
                sh """
                    . ${PYENV}/bin/activate
                    python3 ml/predict.py
                """
            }
        }

        stage('Anomaly Detection') {
            steps {
                sh """
                    . ${PYENV}/bin/activate
                    python3 ml/anomaly_detection.py \
                        --build ${build_time} \
                        --test ${test_time} \
                        --deploy ${deploy_time}
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline + ML feedback completed successfully!"
        }
        failure {
            echo "Pipeline failed."
        }
    }
}
