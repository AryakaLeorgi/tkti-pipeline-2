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

        stage('Run Tests (simulate random failure)') {
            steps {
                script {
                    // This writes a fake log file to simulate a real CI error
                    writeFile file: 'build_error.log', text: 'Simulated Webpack failure'

                    // Forces a failure so the AI auto-fix triggers
                    error("Simulated CI failure: Webpack compilation error.")
                }
            }
        }
    }

    post {
        failure {
            echo "Build failed. Generating AI patch..."

            script {
                // 1. Send logs to your AI patch-server
                sh """
                    echo "Sending logs to AI server at /patch"

                    curl -s -X POST http://localhost:3000/patch \
                        -H "Content-Type: application/json" \
                        -d "{ \\"logs\\": \\"$(cat build_error.log | sed 's/"/\\\\\\"/g')\\" }" \
                        > ai_patch.json

                    echo "AI patch JSON:"
                    cat ai_patch.json
                """

                // 2. Extract patch from JSON safely (using jq)
                sh """
                    echo "Extracting patch using jq..."
                    jq -r '.patch' ai_patch.json > ai_patch_raw.txt
                """

                // 3. Extract diff block only
                sh """
                    echo "Filtering actual diff..."
                    sed -n '/PATCH_START/,/PATCH_END/p' ai_patch_raw.txt \
                        | sed '/PATCH_START/d;/PATCH_END/d' \
                        > ai_fix.diff
                """

                // 4. If empty, skip auto-fix
                def patchExists = sh(
                    script: "test -s ai_fix.diff && echo 1 || echo 0",
                    returnStdout: true
                ).trim()

                if (patchExists == "0") {
                    echo "AI returned no usable patch. Skipping auto-fix."
                    return
                }

                // 5. Validate patch first
                sh "git apply --check ai_fix.diff"

                // 6. Apply patch
                sh "git apply ai_fix.diff"

                // 7. Commit fix to new branch
                def branch = "ai-fix-${env.BUILD_NUMBER}"

                sh """
                    git config user.email "jenkins@local"
                    git config user.name "Jenkins AI Bot"

                    git checkout -b ${branch}
                    git add -A
                    git commit -m 'ci: apply AI auto-fix patch'
                """

                // 8. Push fix to GitHub
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'TOKEN')]) {
                    sh """
                        echo "Pushing branch ${branch} to GitHub..."
                        git push https://${TOKEN}@github.com/AryakaLeorgi/tkti-pipeline-2.git ${branch}
                    """

                    // 9. Create PR via GitHub CLI
                    sh """
                        echo "${TOKEN}" | gh auth login --with-token

                        gh pr create \
                            --title "AI Auto-Fix for CI Failure #${env.BUILD_NUMBER}" \
                            --body "This PR contains an AI-generated patch that fixes the failing build." \
                            --base main \
                            --head ${branch}
                    """
                }

                echo "🎉 AI Patch PR successfully created!"
            }
        }
    }
}
