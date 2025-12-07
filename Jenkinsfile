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

            echo "[AI] Starting patch server..."
            # Kill old instance if exists
            if [ -f /var/lib/jenkins/patch_server.pid ]; then
              kill $(cat /var/lib/jenkins/patch_server.pid) || true
            fi

            # Run server in background & capture real PID
            nohup env GEMINI_API_KEY=$GEMINI_API_KEY node patch-server.js > /var/lib/jenkins/patch_server.log 2>&1 &

            echo $! > /var/lib/jenkins/patch_server.pid
            echo "[AI] Patch server started with PID $(cat /var/lib/jenkins/patch_server.pid)"

            sleep 3

            echo "[AI] Checking server health"
            curl -f http://localhost:3000/health || (echo "[AI] Health check failed" && exit 1)
          '''
        }
      }
    }

    stage('Run Tests (simulate failure)') {
      steps {
        script {
          writeFile file: "test-output.log", text: "Simulated CI failure: Webpack compilation error."
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
        def logs = readFile('test-output.log')

        writeFile file: "ai_request.json", text: "{\"logs\": ${logs.inspect()} }"
        echo "[AI] Sending logs to patch server..."

        sh '''
          set -e
          RESPONSE=$(curl -s -f -X POST http://localhost:3000/patch \
            -H "Content-Type: application/json" \
            -d @ai_request.json)

          echo "$RESPONSE" > ai_patch.json
        '''
      }

      echo "[AI] Patch received."

      script {
        def json = readJSON file: "ai_patch.json"
        writeFile file: "patch.diff", text: json.patch
      }

      sh '''
        git config user.email "ai-bot@example.com"
        git config user.name "AI Bot"

        git checkout -b ai-auto-fix

        git apply patch.diff || true
        git add -A
        git commit -m "AI Auto Fix"
        git push -f origin ai-auto-fix
      '''

      echo "AI Patch ready. Open a PR manually (or enable auto-PR plugin)."
    }
  }
}
