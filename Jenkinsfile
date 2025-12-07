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
        failure {
            echo "==== Build Failed — Running AI Auto-Fix ===="

            script {

                // 1. Send logs to patch server
                sh '''
                    echo "[AI] Sending logs to patch server..."

                    LOGS=$(sed 's/"/\\\\\\"/g' build_error.log)

                    curl -s -X POST http://localhost:3000/patch \
                        -H "Content-Type: application/json" \
                        -d "{ \\"logs\\": \\"$LOGS\\" }" \
                        > ai_patch.json

                    echo "[AI] Response from server:"
                    cat ai_patch.json
                '''

                // 2. Extract patch
                sh '''
                    jq -r ".patch" ai_patch.json > ai_patch_raw.txt
                '''

                // 3. Clean patch content
                sh '''
                    sed -n "/PATCH_START/,/PATCH_END/p" ai_patch_raw.txt \
                        | sed "/PATCH_START/d;/PATCH_END/d" \
                        > ai_fix.diff
                '''

                // 4. Check if patch generated
                def exists = sh(
                    script: "test -s ai_fix.diff && echo 1 || echo 0",
                    returnStdout: true
                ).trim()

                if (exists == "0") {
                    echo "[AI] No patch generated — skipping."
                    return
                }

                // 5. Validate patch
                sh '''
                    echo "[AI] Validating patch..."
                    git apply --check ai_fix.diff
                '''

                // 6. Apply patch
                sh '''
                    echo "[AI] Applying patch..."
                    git apply ai_fix.diff
                '''

                // 7. Create branch + commit
                def branch = "ai-fix-${env.BUILD_NUMBER}"

                sh """
                    git config user.email "jenkins@local"
                    git config user.name "Jenkins AI Bot"

                    git checkout -b ${branch}
                    git add -A
                    git commit -m 'ci: auto-applied AI patch'
                """

                // 8. Push + open PR using GitHub token
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'TOKEN')]) {
                    sh """
                        echo "[AI] Pushing to GitHub..."
                        git push https://${TOKEN}@github.com/AryakaLeorgi/tkti-pipeline-2.git ${branch}

                        echo "${TOKEN}" | gh auth login --with-token

                        gh pr create \
                            --title "AI Auto-Fix for Build #${env.BUILD_NUMBER}" \
                            --body "This PR contains an automatic AI-generated fix." \
                            --base main \
                            --head ${branch}
                    """
                }

                echo "==== AI Fix PR Created Successfully ===="
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
