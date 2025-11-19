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
                    build_time = measureTime {
                        sh '''
                        echo "Running build..."
                        python3 ml/failure_simulation.py build
                        '''
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    test_time = measureTime {
                        sh '''
                        echo "Running tests..."
                        python3 ml/failure_simulation.py test
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    deploy_time = measureTime {
                        sh '''
                        echo "Deploying..."
                        python3 ml/failure_simulation.py deploy
                        '''
                    }
                }
            }
        }

        stage('Log Real Metrics') {
            steps {
                sh '''
                . .venv/bin/activate
                python3 ml/log_real_metrics.py --build ${build_time} --test ${test_time} --deploy ${deploy_time}
                '''
            }
        }
    }
}


def measureTime(Closure body) {
    def start = System.currentTimeMillis()
    body()
    def end = System.currentTimeMillis()
    return ((end - start) / 1000.0) // return seconds
}
