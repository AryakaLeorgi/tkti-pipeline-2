pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/AryakaLeorgi/tkti-pipeline-2.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build Simulation') {
            steps {
                echo 'Building the project... (simulated build)'
            }
        }

        stage('Deploy Simulation') {
            steps {
                echo 'Deploying to staging environment... (simulated deploy)'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}

