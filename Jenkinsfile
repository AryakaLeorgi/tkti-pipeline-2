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

        stage('Run Anomaly Detection') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python3 ml/anomaly_check.py
                '''
            }
        }

        stage('AI Anomaly Stress Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python3 ml/stress_test.py
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
