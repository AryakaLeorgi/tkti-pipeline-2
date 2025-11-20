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
                    python3 ml/detect_anomaly.py
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

    stage('AI Auto Fix') {
    when { expression { return currentBuild.result == 'FAILURE' } }
    steps {
        sh '''
        . .venv/bin/activate
        export GROQ_API_KEY=$GROQ_API_KEY
        python3 ml/auto_fix_code.py "$PIPELINE_ERROR" > ai_fix.txt
        '''
        echo readFile('ai_fix.txt')
    }
}


    post {
        always {
            echo "Pipeline finished."
        }
    }
}
