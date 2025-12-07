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

stage('Test Gemini Key') {
    steps {
        sh '''
            echo "Testing Gemini API key..."
            curl -s -H "Content-Type: application/json" \
                -H "x-goog-api-key: $GEMINI_API_KEY" \
                -d '{"contents":[{"parts":[{"text":"hello"}]}]}' \
                https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent \
                -o gemini_test_response.json

            echo "Response from Gemini:"
            cat gemini_test_response.json
        '''
    }
}


stage('Start AI Patch Server') {
    steps {
        sh '''
            cd explain-error
            npm install

            # Start server WITH GEMINI_API_KEY injected
            nohup env GEMINI_API_KEY=$GEMINI_API_KEY node patch-server.js \
                > ai_patch_server.log 2>&1 &

            sleep 2
        '''
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

            // 1. Send logs to AI patch server
            sh '''
                echo "Sending logs to AI server..."
                curl -s -X POST http://localhost:3000/patch \
                    -H "Content-Type: application/json" \
                    -d "{ \\"logs\\": \\"$(sed 's/"/\\\\\\"/g' build_error.log)\\" }" \
                    > ai_patch.json

                echo "AI response:"
                cat ai_patch.json
            '''

            // 2. Extract patch using jq
            sh '''
                echo "Extracting patch..."
                jq -r ".patch" ai_patch.json > ai_patch_raw.txt
            '''

            // 3. Extract only PATCH block
            sh '''
                echo "Filtering diff..."
                sed -n "/PATCH_START/,/PATCH_END/p" ai_patch_raw.txt \
                    | sed "/PATCH_START/d;/PATCH_END/d" \
                    > ai_fix.diff
            '''

            // 4. Check if patch exists
            def exists = sh(
                script: "test -s ai_fix.diff && echo 1 || echo 0",
                returnStdout: true
            ).trim()

            if (exists == "0") {
                echo "No AI patch found. Skip."
                return
            }

            // 5. Validate patch
            sh 'git apply --check ai_fix.diff'

            // 6. Apply patch
            sh 'git apply ai_fix.diff'

            // 7. Create branch + commit
            def branch = "ai-fix-${env.BUILD_NUMBER}"
            sh """
                git config user.email "jenkins@local"
                git config user.name "Jenkins AI Bot"

                git checkout -b ${branch}
                git add -A
                git commit -m 'ci: apply AI auto fix patch'
            """

            // 8. Push + PR
            withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'TOKEN')]) {
                sh """
                    git push https://${TOKEN}@github.com/AryakaLeorgi/tkti-pipeline-2.git ${branch}
                    echo "${TOKEN}" | gh auth login --with-token

                    gh pr create \
                        --title "AI Auto-Fix for CI Failure #${env.BUILD_NUMBER}" \
                        --body "This PR has an AI-generated patch to fix the failed build." \
                        --base main \
                        --head ${branch}
                """
            }

            echo "AI Fix PR created!"
        }
    }
}

}
