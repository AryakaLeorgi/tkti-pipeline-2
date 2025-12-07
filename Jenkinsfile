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
stage("Start AI Patch Server") {
    steps {
        withCredentials([string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_KEY')]) {

            sh """
                echo "[AI] Installing dependencies for patch server..."
                cd explain-error
                npm install

                echo "[AI] Starting patch server with Gemini key..."

                nohup env GEMINI_API_KEY=\${GEMINI_KEY} node patch-server.js \
                    > /var/lib/jenkins/ai_patch_server.log 2>&1 &

                echo \$! > /var/lib/jenkins/patch_server.pid
                sleep 2
                echo "[AI] Patch server PID: \$(cat /var/lib/jenkins/patch_server.pid)"
            """
        }
    }
}

        /* ------------------------------
         * SIMULATED FAILURE
         * ------------------------------ */
        stage("Run Tests (simulate failure)") {
            steps {
                script {
                    writeFile file: "build_error.log", text: "Simulated Webpack failure\n"
                    error("Simulated CI failure: Webpack compilation error.")
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
            sh """
                echo "[AI] Sending logs to patch server..."

                # Escape quotes for JSON
                sed 's/\"/\\\\\"/g' build_error.log > logs.tmp

                # Send logs directly
                curl -s -X POST http://localhost:3000/patch \
                    -H "Content-Type: application/json" \
                    -d "{ \\"logs\\": \\"$(cat logs.tmp)\\" }" \
                    > ai_patch.json

                echo "[AI] Response:"
                cat ai_patch.json
            """

            // Cleanup patch server
            sh """
                echo "[AI] Cleaning up patch server..."
                if [ -f /var/lib/jenkins/patch_server.pid ]; then
                    kill \$(cat /var/lib/jenkins/patch_server.pid)
                    rm /var/lib/jenkins/patch_server.pid
                fi
            """
        }
    }
}

}
