pipeline {
  agent any

  environment {
    GEMINI_KEY = credentials('GEMINI_KEY')
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install Dependencies') {
      steps {
        sh '''
          cd src
          npm install
        '''
      }
    }

    stage('Start AI Patch Server') {
      steps {
        withCredentials([string(credentialsId: 'GEMINI_KEY', variable: 'GEMINI_API_KEY')]) {
          sh '''
            echo "[AI] Installing dependencies for patch server..."
            cd explain-error
            npm install

            echo "[AI] Killing old instance if exists..."
            if [ -f /var/lib/jenkins/patch_server.pid ]; then
              kill $(cat /var/lib/jenkins/patch_server.pid) || true
              rm /var/lib/jenkins/patch_server.pid
            fi

            echo "[AI] Starting patch server..."
            nohup env GEMINI_API_KEY=$GEMINI_API_KEY node patch-server.js \
              > /var/lib/jenkins/patch_server.log 2>&1 &

            echo $! > /var/lib/jenkins/patch_server.pid
            echo "[AI] Patch server started with PID $(cat /var/lib/jenkins/patch_server.pid)"

            sleep 3

            echo "[AI] Checking server health..."
            curl --retry 5 --retry-delay 2 -f http://localhost:3000/health
          '''
        }
      }
    }

    stage('Run Tests (simulate failure)') {
      steps {
        script {
          writeFile file: "test-output.log",
                    text: "Simulated CI failure: Webpack compilation error."

          error("Simulated CI failure: Webpack compilation error.")
        }
      }
    }
  }

  post {
    failure {

      echo "==== Build Failed — Running AI Auto-Fix ===="

      script {
        echo "[AI] Reading logs..."
        def logs = readFile("test-output.log")

        // CORRECT JSON ENCODING
        def json = [ logs: logs ]
        writeJSON file: "ai_request.json", json: json, pretty:  false

        echo "[AI] Sending logs to patch server..."
        sh '''
          curl -s -X POST http://localhost:3000/patch \
            -H "Content-Type: application/json" \
            -d @ai_request.json > ai_patch.json || echo "{}" > ai_patch.json
        '''
      }

      echo "[AI] Patch received."

      script {
        def resp = readJSON file: "ai_patch.json"
        writeFile file: "patch.diff", text: resp.patch ?: "# No patch"
      }

      sh '''
        set +e

        git config user.email "ai-bot@example.com"
        git config user.name "AI Bot"

        git checkout -B ai-auto-fix

        echo "[AI] Applying patch..."
        git apply patch.diff || echo "[AI] Patch failed to apply, continuing anyway."

        git add -A
        git commit -m "AI Auto Fix" || echo "[AI] Nothing to commit."

        echo "[AI] Pushing branch..."
        git push -f origin ai-auto-fix || true
      '''

      echo "AI patch pushed to branch: ai-auto-fix"
    }
  }
}
