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

                        // --- BUILD ---
                        def buildOutput = sh(script: "python3 ml/failure_simulation.py build", returnStdout: true).trim()
                        echo buildOutput
                        def buildTime = buildOutput.find(/Duration: ([0-9.]+)s/) { full, num -> num }
                        env.BUILD_TIME = buildTime

                        // --- TEST ---
                        def testOutput = sh(script: "python3 ml/failure_simulation.py test", returnStdout: true).trim()
                        echo testOutput
                        def testTime = testOutput.find(/Duration: ([0-9.]+)s/) { full, num -> num }
                        env.TEST_TIME = testTime

                        // --- DEPLOY ---
                        def deployOutput = sh(script: "python3 ml/failure_simulation.py deploy", returnStdout: true).trim()
                        echo deployOutput
                        def deployTime = deployOutput.find(/Duration: ([0-9.]+)s/) { full, num -> num }
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
