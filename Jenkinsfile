pipeline {
    agent any

    environment {
        // Path virtualenv
        VENV = ".venv"
    }

    stages {

        stage('Setup Python Env') {
            steps {
                sh '''
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r ml/requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                script {
                    def start = System.currentTimeMillis()
                    sh 'echo Building project...'
                    sleep 1
                    env.BUILD_TIME = ((System.currentTimeMillis() - start) / 1000).toString()
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    def start = System.currentTimeMillis()
                    sh 'echo Running tests...'
                    sleep 1
                    env.TEST_TIME = ((System.currentTimeMillis() - start) / 1000).toString()
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def start = System.currentTimeMillis()
                    sh 'echo Deploying...'
                    sleep 1
                    env.DEPLOY_TIME = ((System.currentTimeMillis() - start) / 1000).toString()
                }
            }
        }

        stage('ML Training') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    python3 ml/train_model.py
                '''
            }
        }

        stage('ML Evaluation') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    python3 ml/evaluate_pipeline.py > optimization_report.txt
                '''
            }
        }

        stage('ML Optimizer') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    python3 ml/optimizer.py >> optimization_report.txt
                '''
            }
        }

        stage('Save Real Metrics') {
            steps {
                script {
                    // Save success/failed result
                    env.PIPELINE_RESULT = currentBuild.currentResult
                }

                sh '''
                    . $VENV/bin/activate
                    python3 ml/log_real_metrics.py
                '''
            }
        }

        stage('Anomaly Detection') {
            steps {
                sh '''
                    . $VENV/bin/activate
                    python3 ml/detect_anomaly.py
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'optimization_report.txt', fingerprint: true
                archiveArtifacts artifacts: 'data/*.csv', fingerprint: true
            }
        }
    }

    post {
        always {
            echo "Pipeline completed with result: ${currentBuild.currentResult}"
        }
    }
}
