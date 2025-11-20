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

            def simulateStage = { stageName ->

                // Jalankan simulation (aman walaupun exit 1)
                def output = sh(
                    script: "python3 ml/failure_simulation.py ${stageName}",
                    returnStdout: true
                ).trim()

                echo output

                // Ambil exit code di panggilan terpisah
                def status = sh(
                    script: "python3 ml/failure_simulation.py ${stageName}",
                    returnStatus: true
                )

                // Extract duration dari output pertama
                def duration = output.find(/Duration: ([0-9.]+)s/) { full, num -> num }

                // 1 = success, 0 = fail
                def successFlag = (status == 0 ? 1 : 0)

                return [duration, successFlag]
            }

            def b = simulateStage("build")
            env.BUILD_TIME = b[0]
            env.BUILD_SUCCESS = b[1]

            def t = simulateStage("test")
            env.TEST_TIME = t[0]
            env.TEST_SUCCESS = t[1]

            def d = simulateStage("deploy")
            env.DEPLOY_TIME = d[0]
            env.DEPLOY_SUCCESS = d[1]

            echo """
Metrics:
  BUILD:  time=${env.BUILD_TIME}, success=${env.BUILD_SUCCESS}
  TEST:   time=${env.TEST_TIME},  success=${env.TEST_SUCCESS}
  DEPLOY: time=${env.DEPLOY_TIME}, success=${env.DEPLOY_SUCCESS}
"""
        }
    }
}


        stage('Run Anomaly Detection') {
            steps {
                sh """
                . .venv/bin/activate
                python3 ml/detect_anomaly.py \
                    $BUILD_TIME $TEST_TIME $DEPLOY_TIME \
                    $BUILD_SUCCESS $TEST_SUCCESS $DEPLOY_SUCCESS
                """
            }
        }

        stage('AI Anomaly Stress Test') {
            when {
                expression { true } // always run even if anomaly or failure happened
            }
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
