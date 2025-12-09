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
                echo "[AI] Patch received:"
                echo diffContent
                
                // Try multiple patch apply strategies
                def patchApplied = sh(
                    script: '''
                        echo "[AI] Attempting to apply patch..."
                        
                        # Strategy 1: Normal apply
                        if git apply --check ai_fix.diff 2>/dev/null; then
                            echo "[AI] Patch check passed, applying..."
                            git apply -v ai_fix.diff && echo "PATCH_SUCCESS" && exit 0
                        fi
                        
                        # Strategy 2: Try with --3way for conflicts
                        echo "[AI] Trying --3way merge..."
                        if git apply --3way ai_fix.diff 2>/dev/null; then
                            echo "PATCH_SUCCESS" && exit 0
                        fi
                        
                        # Strategy 3: Try ignoring whitespace
                        echo "[AI] Trying with whitespace ignore..."
                        if git apply --ignore-whitespace ai_fix.diff 2>/dev/null; then
                            echo "PATCH_SUCCESS" && exit 0
                        fi
                        
                        echo "[AI] All patch strategies failed"
                        echo "PATCH_FAILED"
                    ''',
                    returnStdout: true
                ).trim()
                
                def patchSuccess = patchApplied.contains("PATCH_SUCCESS")
                echo "[AI] Patch applied successfully: ${patchSuccess}"

                def branch = "ai-fix-${env.BUILD_NUMBER}"

                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GHTOKEN')]) {
                    
                    sh """
                        git config user.email "ai-bot@autofix"
                        git config user.name "AI Auto Fix Bot"
                        
                        # Create new branch for the fix
                        git checkout -b ${branch} || git checkout ${branch}
                        
                        # Reset ALL staged changes first
                        git reset HEAD . 2>/dev/null || true
                    """
                    
                    // Use Groovy logic to determine what to add
                    if (patchSuccess) {
                        echo "[AI] Patch was successful, adding src/auth.js..."
                        sh "git add src/auth.js 2>/dev/null || true"
                    } else {
                        echo "[AI] Patch failed, adding diagnostic.md..."
                        sh "git add diagnostic.md 2>/dev/null || true"  
                    }
                    
                    sh """
                        # Explicitly REMOVE any unwanted files from staging
                        git reset HEAD src/package-lock.json 2>/dev/null || true
                        git reset HEAD src/package.json 2>/dev/null || true
                        git reset HEAD package-lock.json 2>/dev/null || true
                        git reset HEAD node_modules 2>/dev/null || true
                        git reset HEAD src/node_modules 2>/dev/null || true
                        
                        # Show what files are staged
                        echo "[AI] Files staged for commit:"
                        git diff --cached --name-only
                        
                        # Check if there are changes to commit
                        if git diff --cached --quiet; then
                            echo "[AI] No changes to commit"
                        else
                            git commit -m "AI Auto-Fix: ${patchSuccess ? 'Fixed typo in auth.js (.tset -> .test)' : 'Build failure diagnostic'}"
                            git push https://\${GHTOKEN}@github.com/${GH_REPO}.git ${branch} --force
                            echo "[AI] ✅ Changes pushed to branch: ${branch}"
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
