pipeline {
    agent any

    environment {
        NODE_OPTIONS = "--max-old-space-size=512"
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
            environment {
                GEMINI_API_KEY = credentials('gemini-key')
            }
            steps {
                sh """
                echo "[AI] Installing dependencies..."
                cd explain-error
                npm install

                echo "[AI] Starting patch server..."
                nohup env GEMINI_API_KEY=\$GEMINI_API_KEY node patch-server.js > patch.log 2>&1 &

                echo \$! > /var/lib/jenkins/patch_server.pid

                sleep 2

                # Health check with retries
                for i in {1..10}; do
                    echo "[AI] Waiting for /health..."
                    curl -s http://localhost:3000/health && break
                    sleep 1
                done
                """
            }
        }

        stage('Run Tests (simulate failure)') {
            steps {
                script {
                    writeFile file: "build.log", text: "Simulated CI failure: Webpack compilation error.\n"
                    error("Simulated CI failure: Webpack compilation error.")
                }
            }
        }
    }

    post {
        failure {

            echo "==== Build Failed — Running AI Auto-Fix ===="

            script {
                def logs = readFile("build.log")
                writeFile file: "ai_request.json", text: "{ \"logs\": \"${logs.replace('"','\\"')}\" }"

                echo "[AI] Sending logs…"

                sh """
                curl -s -X POST http://localhost:3000/patch \
                    -H "Content-Type: application/json" \
                    -d @ai_request.json > ai_patch.json
                """

                echo "[AI] Patch response:"
                sh "cat ai_patch.json"

                def patch = readFile("ai_patch.json")

                if (!patch.contains('---')) {
                    echo "[AI] Invalid patch (no diff markers). Skipping PR."
                } else {
                    echo "[AI] Patch OK. (PR creation step would go here.)"
                }
            }

            echo "[AI] Cleaning up patch server…"

            sh """
            if [ -f /var/lib/jenkins/patch_server.pid ]; then
                kill \$(cat /var/lib/jenkins/patch_server.pid) || true
                rm /var/lib/jenkins/patch_server.pid
            fi
            """
        }
    }
}
