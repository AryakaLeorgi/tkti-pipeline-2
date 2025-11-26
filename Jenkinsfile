pipeline {
    agent any

    environment {
        PYTHON = "/usr/bin/python3"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/AryakaLeorgi/tkti-pipeline-2.git', branch: 'main'
            }
        }

        stage('Setup Python Env') {
            steps {
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run TKTI Analysis') {
            steps {
                sh """
                    . venv/bin/activate
                    python src/main.py --input build.xml --output report.json
                """
            }
        }

        stage('Run Sandbox Build') {
            steps {
                sh """
                    docker build -f docker/Dockerfile.sandbox -t tkti-sandbox .
                    docker run --rm -v \$PWD:/workspace tkti-sandbox
                """
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'report.json', fingerprint: true
            }
        }
    }
}
