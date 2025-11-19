pipeline {
    agent any

    stages {

        stage('Setup Python Env') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                script {
                    echo "Running build..."
                    sh "python3 ml/failure_simulation.py build"

                    build_time = sh(script: "grep DURATION: build.log | awk '{print \$2}'", returnStdout: true).trim()
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "Running tests..."
                    sh "python3 ml/failure_simulation.py test"

                    test_time = sh(script: "grep DURATION: test.log | awk '{print \$2}'", returnStdout: true).trim()
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Deploying..."
                    sh "python3 ml/failure_simulation.py deploy"

                    deploy_time = sh(script: "grep DURATION: deploy.log | awk '{print \$2}'", returnStdout: true).trim()
                }
            }
        }

        stage('Log Real Metrics') {
            steps {
                script {
                    sh """
                        . .venv/bin/activate
                        python3 ml/log_real_metrics.py --build ${build_time} --test ${test_time} --deploy ${deploy_time}
                    """
                }
            }
        }

        stage('Train ML Model') {
            steps {
                script {
                    sh """
                        . .venv/bin/activate
                        python3 ml/train_model.py
                    """
                }
            }
        }

        stage('Anomaly Detection') {
            steps {
                script {
                    sh """
                        . .venv/bin/activate
                        python3 ml/detect_anomaly.py ${build_time} ${test_time} ${deploy_time}
                    """
                }
            }
        }
    }
}
