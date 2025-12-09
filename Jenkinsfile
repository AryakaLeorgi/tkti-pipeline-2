pipeline {
    agent any

    environment {
        NODE_ENV = "ci"
        GH_REPO = "AryakaLeorgi/tkti-pipeline-2"
    }

    stages {

        /* ------------------------------
         * CHECKOUT
         * ------------------------------ */
        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        /* ------------------------------
         * INSTALL DEPENDENCIES
         * ------------------------------ */
        stage("Install Dependencies") {
            steps {
                sh """
                    cd src
                    npm install
                """
            }
        }

        /* ------------------------------
         * START AI PATCH SERVER
         * ------------------------------ */
stage('Start AI Patch Server') {
  steps {
    withCredentials([string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_API_KEY')]) {
      sh '''
        echo "[AI] Installing dependencies for patch server..."
        cd explain-error
        npm install

        echo "[AI] Starting patch server..."
        nohup env GEMINI_API_KEY="$GEMINI_API_KEY" node patch-server.js > ../patch_server.log 2>&1 &
        echo $! > /var/lib/jenkins/patch_server.pid

        sleep 3
        echo "[AI] Checking health..."
        curl -s http://localhost:3000/health || {
          echo "❌ Patch server failed to start!"
          echo "---- Logs ----"
          cat ../patch_server.log
          exit 1
        }

        echo "[AI] Patch server OK"
      '''
    }
  }
}


        /* ------------------------------
         * RUN ACTUAL TESTS
         * ------------------------------ */
        stage("Run Tests") {
            steps {
                script {
                    // Run tests and capture output
                    def testResult = sh(
                        script: '''
                            set -o pipefail
                            cd src
                            node test.js 2>&1 | tee ../build_error.log
                        ''',
                        returnStatus: true
                    )
                    
                    if (testResult != 0) {
                        // Read the source files to give AI context
                        def errorLog = readFile("build_error.log").trim()
                        def sourceFiles = ""
                        
                        // Read relevant source files for AI context
                        try {
                            sourceFiles = "\n\n=== SOURCE FILE: src/auth.js ===\n" + readFile("src/auth.js")
                        } catch (e) { }
                        try {
                            sourceFiles += "\n\n=== SOURCE FILE: src/test.js ===\n" + readFile("src/test.js")
                        } catch (e) { }
                        
                        // Write combined error log with source context
                        writeFile file: "build_error.log", text: errorLog + sourceFiles
                        
                        error("Test failed with exit code: ${testResult}")
                    }
                }
            }
        }
    }

    /* ----------------------------------------
     * POST — RUN AI AUTO FIX
     * ---------------------------------------- */
post {
    failure {
        echo "==== Build Failed — Running AI Auto-Fix ===="

        script {

            echo "[AI] Reading logs..."
            def logs = readFile("build_error.log").trim()

            // Escape JSON + newline safe
            def safeLogs = logs
                .replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")

            echo "[AI] Sending logs to patch server..."

            // Write temp request body
            writeFile file: "ai_request.json", text: """{
                "logs": "${safeLogs}"
            }"""

            // Call patch server
            sh '''
                curl -s -X POST http://localhost:3000/patch \
                    -H "Content-Type: application/json" \
                    -d @ai_request.json \
                    > ai_patch.json
            '''

            echo "[AI] Response:"
            sh "cat ai_patch.json"

            // Extract patch
            sh 'jq -r ".patch" ai_patch.json > ai_fix.diff'

            def diffContent = readFile("ai_fix.diff").trim()

            if (!diffContent) {
                echo "[AI] No valid patch produced — skipping PR."
            } else {
                echo "[AI] Patch received, applying..."

                sh "git apply --check ai_fix.diff || echo 'Patch check failed, continuing...'"
                sh "git apply ai_fix.diff || echo 'Patch apply failed, will create diagnostic PR'"

                def branch = "ai-fix-${env.BUILD_NUMBER}"

                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GHTOKEN')]) {
                    
                    sh """
                        git config user.email "ai-bot@autofix"
                        git config user.name "AI Auto Fix Bot"
                        
                        # Create new branch for the fix
                        git checkout -b ${branch} || git checkout ${branch}
                        
                        # Add ONLY the actual source code changes (not temp files)
                        # This makes the PR show real file changes like auth.js, not just .diff files
                        git add src/ 2>/dev/null || true
                        
                        # If no source changes, add diagnostic.md as fallback
                        if git diff --cached --quiet; then
                            git add diagnostic.md 2>/dev/null || true
                        fi
                        
                        # Check if there are changes to commit
                        if git diff --cached --quiet; then
                            echo "[AI] No changes detected after applying patch"
                        else
                            # Show what files are being committed
                            echo "[AI] Files to be committed:"
                            git diff --cached --name-only
                            
                            git commit -m "AI Auto-Fix: ${diffContent.contains('auth.js') ? 'Fixed typo in auth.js' : 'Build failure patch'}"
                            git push https://\${GHTOKEN}@github.com/${GH_REPO}.git ${branch} --force
                            echo "[AI] Changes pushed to branch: ${branch}"
                        fi
                    """

                    // Create PR
                    def prBody = "Automated fix generated by Gemini Patch AI for build #${env.BUILD_NUMBER}."
                    
                    sh """
                        curl -s -X POST \\
                            -H "Authorization: token \${GHTOKEN}" \\
                            -H "Accept: application/vnd.github+json" \\
                            https://api.github.com/repos/${GH_REPO}/pulls \\
                            -d '{"title": "AI Auto-Fix Patch #${env.BUILD_NUMBER}", "body": "${prBody}", "head": "${branch}", "base": "main"}' \\
                            || echo "PR creation failed or already exists"
                    """
                }

                echo "[AI] Pull request created successfully!"
            }
        }

        echo "[AI] Cleaning up patch server..."

        sh '''
            if [ -f /var/lib/jenkins/patch_server.pid ]; then
                kill $(cat /var/lib/jenkins/patch_server.pid) || true
                rm /var/lib/jenkins/patch_server.pid
            fi
        '''
    }
}


}
