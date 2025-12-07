pipeline {
    agent any

    stages {

        stage('Install Explain Error Service') {
            steps {
                sh '''
                    cd explain-error
                    npm install
                '''
            }
        }

        stage('Start Explain Error Service') {
            steps {
                sh '''
                    cd explain-error
                    nohup node server.js > explain.log 2>&1 &
                    echo $! > explain.pid
                '''
            }
        }

        stage('Run CI/CD Simulation') {
            steps {
                script {
                    echo "Simulating random failure..."

                    // Random fail
                    def fail = new Random().nextInt(3)

                    if (fail == 0) {
                        error("Random Failure: Dependency installation failed")
                    } else if (fail == 1) {
                        error("Random Failure: Unit test crashed")
                    } else {
                        error("Random Failure: Code build failed")
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
                // Collect last 2000 lines of logs
                def logs = currentBuild.rawBuild.getLog(2000).join("\n")

                // Send to your explain-error service
                def response = httpRequest(
                    httpMode: 'POST',
                    url: "http://localhost:3000/explain",
                    contentType: 'APPLICATION_JSON',
                    requestBody: groovy.json.JsonOutput.toJson([logs: logs])
                )

                echo "AI Explanation:"
                echo response.content
            }
        }

        always {
            sh '''
                if [ -f explain-error/explain.pid ]; then
                    kill $(cat explain-error/explain.pid) || true
                fi
            '''
        }
    }
}
