pipeline {
    agent any

    stages {
        stage('Prepare Python Env') {
            steps {
                sh '''
                    echo "[INFO] Creating virtual environment..."
                    python3 -m venv .venv
                    . .venv/bin/activate

                    echo "[INFO] Install dependencies..."
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    echo "[INFO] Environment ready."
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                    echo "[INFO] Training model..."
                    . .venv/bin/activate
                    python3 ml/train_model.py
                '''
            }
        }

        stage('Detect Anomaly') {
            steps {
                sh '''
                    echo "[INFO] Running anomaly detection..."
                    . .venv/bin/activate
                    python3 ml/detect_anomaly.py
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
