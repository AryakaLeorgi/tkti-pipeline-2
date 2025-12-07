pipeline {
agent any

```
environment {
    NODEJS_HOME = "/usr/bin"
    PATH = "${NODEJS_HOME}:${env.PATH}"
    GEMINI_API_KEY = credentials('GEMINI_API_KEY')
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
            sh '''
                cd explain-error
                npm install

                # Start server
                nohup env GEMINI_API_KEY=$GEMINI_API_KEY node patch-server.js \
                    > ~/ai_patch_server.log 2>&1 &

                sleep 2
            '''
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
        echo "Build failed. Generating AI patch..."

        script {
            // 1. Send logs → Gemini
            sh '''
                echo "Sending logs to AI server..."

                curl -s -X POST http://localhost:3000/patch \
                    -H "Content-Type: application/json" \
                    -d "{ \\"logs\\": \\"$(sed 's/"/\\\\\\"/g' build_error.log)\\" }" \
                    > ai_patch.json

                echo "AI response:"
                cat ai_patch.json
            '''

            // 2. Extract patch text
            sh '''
                jq -r ".patch" ai_patch.json > ai_patch_raw.txt
            '''

            // 3. Filter unified diff block
            sh '''
                sed -n "/PATCH_START/,/PATCH_END/p" ai_patch_raw.txt \
                    | sed "/PATCH_START/d;/PATCH_END/d" \
                    > ai_fix.diff
            '''

            // 4. check if patch exists
            def exists = sh(
                script: "test -s ai_fix.diff && echo 1 || echo 0",
                returnStdout: true
            ).trim()

            if (exists == "0") {
                echo "No AI patch found. Skipping auto-fix."
                return
            }

            // 5. validate and apply patch
            sh 'git apply --check ai_fix.diff'
            sh 'git apply ai_fix.diff'

            // 6. commit + branch
            def branch = "ai-fix-${env.BUILD_NUMBER}"
            sh """
                git config user.email "jenkins@local"
                git config user.name "Jenkins AI Bot"

                git checkout -b ${branch}
                git add -A
                git commit -m 'ci: auto-applied AI patch'
            """

            // 7. push + PR
            withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'TOKEN')]) {
                sh """
                    git push https://${TOKEN}@github.com/AryakaLeorgi/tkti-pipeline-2.git ${branch}
                    echo "${TOKEN}" | gh auth login --with-token

                    gh pr create \
                        --title "AI Auto-Fix for Build #${env.BUILD_NUMBER}" \
                        --body "This PR includes an AI-generated patch." \
                        --base main \
                        --head ${branch}
                """
            }

            echo "AI Fix PR created!"
        }
    }
}
```

}
