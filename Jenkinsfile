pipeline {
    agent any

    stages {

        stage('Setup Python venv') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install --upgrade pip
                pip install pandas scikit-learn joblib
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
                    def buildTime = sh(script: "python3 ml/failure_simulation.py build", returnStdout: true).trim()
                    echo "Build simulation: ${buildTime}"

                    def testTime = sh(script: "python3 ml/failure_simulation.py test", returnStdout: true).trim()
                    echo "Test simulation: ${testTime}"

                    def deployTime = sh(script: "python3 ml/failure_simulation.py deploy", returnStdout: true).trim()
                    echo "Deploy simulation: ${deployTime}"

                    env.BUILD_TIME = buildTime
                    env.TEST_TIME = testTime
                    env.DEPLOY_TIME = deployTime
                }
            }
        }

        stage('Run Anomaly Detection') {
            steps {
                sh '''
                . .venv/bin/activate
                python3 ml/detect_anomaly.py $BUILD_TIME $TEST_TIME $DEPLOY_TIME
                '''
            }
        }

        stage('AI Anomaly Stress Test') {
            steps {
                sh '''
                . .venv/bin/activate
                python3 ml/test_anomaly_model.py
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
    }
}
