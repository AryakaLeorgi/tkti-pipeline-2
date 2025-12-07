pipeline {
    agent any

    environment {
        NODEJS_HOME = "/usr/bin"
        PATH = "${NODEJS_HOME}:${env.PATH}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                    cd src
                    npm install
                """
            }
        }

        stage('Start AI Patch Server') {
            steps {
                withCredentials([string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_API_KEY')]) {
                    sh '''
                        echo "[AI] Installing dependencies for patch server..."
                        cd explain-error
                        npm install

                        echo "[AI] Starting patch server with Gemini key..."
                        nohup env GEMINI_API_KEY=$GEMINI_API_KEY \
                            node patch-server.js > ~/ai_patch_server.log 2>&1 &

                        echo $! > ~/patch_server.pid

                        sleep 2

                        echo "[AI] Patch server PID:"
                        cat ~/patch_server.pid

                        echo "[AI] Patch server logs:"
                        tail -n 20 ~/ai_patch_server.log || true
                    '''
                }
            }
        }

        stage('Run Tests (simulate failure)') {
            steps {
                script {
                    writeFile file: 'build_error.log', text: 'Simulated Webpack failure'
                    error("Simulated CI failure: Webpack compilation error.")
                }
            }
        }
    }

post {
    unsuccessful {
        echo "==== Build Failed — Running AI Auto-Fix ===="

        script {
            sh '''
                echo "[AI] Sending logs to patch server..."

                LOGS=$(sed 's/"/\\\\\\"/g' build_error.log)

                curl -s -X POST http://localhost:3000/patch \
                    -H "Content-Type: application/json" \
                    -d "{ \\"logs\\": \\"$LOGS\\" }" \
                    > ai_patch.json || true

                echo "[AI] Response:"
                cat ai_patch.json || true
            '''

            // (patch apply + pr steps unchanged)
        }
    }

    always {
        echo "Cleaning up patch server..."

        sh '''
            if [ -f ~/patch_server.pid ]; then
                kill $(cat ~/patch_server.pid) || true
                rm ~/patch_server.pid
            fi
        '''
    }
}

}
