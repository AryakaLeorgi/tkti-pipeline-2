pipeline {
    agent any

    environment {
        // Load API key from Jenkins credentials securely
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

        stage('Run Tests (with random failure)') {
            steps {
                script {

                    // Random failure simulation
                    def failReasons = [
                        "Unit test timeout on module A",
                        "Dependency missing: lodash",
                        "SyntaxError: Unexpected token ';'",
                        "TypeError: Cannot read property 'x' of undefined",
                        "Build step failed: webpack compilation error",
                        "ESLint: 23 problems (2 errors, 21 warnings)"
                    ]

                    def chosenFailReason = failReasons[new Random().nextInt(failReasons.size())]

                    // Save the "error" as log file for AI to analyze
                    writeFile file: "build_error.log", text: chosenFailReason

                    // Always mark this stage as failed to trigger explain stage
                    error("Simulated random CI failure: ${chosenFailReason}")
                }
            }
        }
    }
    post {
        failure {
            echo "Build failed. Generating AI explanation..."
            sh '''
                cd explain-error
                npm install
                node explain.js ../build_error.log
            '''
        }
    }

}
