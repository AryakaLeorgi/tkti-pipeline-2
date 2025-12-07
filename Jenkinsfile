pipeline {
    agent any

    environment {
        NODEJS_HOME = "/usr/bin"           // adjust if needed
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

        stage('Run Tests (simulate random failure)') {
            steps {
                script {
                    // Create fake build_error.log
                    writeFile file: 'build_error.log', text: 'Simulated Webpack failure'

                    error("Simulated random CI failure: Build step failed: webpack compilation error")
                }
            }
        }
    }

    post {
        failure {
            echo "Build failed. Generating AI patch..."

            script {
                // 1. Send logs to AI server
                sh """
                    curl -s -X POST http://localhost:3000/patch \
                        -H "Content-Type: application/json" \
                        -d '{ "logs": "Build failed. See build_error.log" }' \
                        > ai_patch.json
                """

                // 2. Extract patch from JSON
                sh """
                    cat ai_patch.json \
                        | sed -n 's/.*"patch": "\(.*\)"/\\1/p' \
                        | sed 's/\\\\n/\\n/g' \
                        > ai_patch_raw.txt
                """

                // 3. Extract diff block only
                sh """
                    sed -n '/PATCH_START/,/PATCH_END/p' ai_patch_raw.txt \
                        | sed '/PATCH_START/d;/PATCH_END/d' \
                        > ai_fix.diff
                """

                // If empty, skip
                def patchExists = sh(script: "test -s ai_fix.diff && echo 1 || echo 0", returnStdout: true).trim()
                if (patchExists == "0") {
                    echo "AI returned no patch. Skipping auto-fix."
                    return
                }

                // 4. Check if patch applies cleanly
                sh "git apply --check ai_fix.diff"

                // 5. Apply the patch
                sh "git apply ai_fix.diff"

                // 6. Commit fix on new branch
                def branch = "ai-fix-${env.BUILD_NUMBER}"
                sh """
                    git config user.email "jenkins@local"
                    git config user.name "Jenkins AI Bot"

                    git checkout -b ${branch}
                    git add -A
                    git commit -m 'ci: apply AI auto fix patch'
                """

                // 7. Push to GitHub
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'TOKEN')]) {
                    sh """
                        git push https://${TOKEN}@github.com/AryakaLeorgi/tkti-pipeline-2.git ${branch}
                    """
                }

                // 8. Create PR using GitHub CLI
                sh """
                    gh auth login --with-token <<< "${TOKEN}"
                    gh pr create \
                        --title "AI Auto-Fix for Build Failure #${env.BUILD_NUMBER}" \
                        --body "This PR contains an AI-generated patch that fixes the failing build." \
                        --base main \
                        --head ${branch}
                """

                echo "AI Patch PR successfully created!"
            }
        }
    }
}
