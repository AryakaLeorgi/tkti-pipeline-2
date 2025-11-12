pipeline {
    agent any

    environment {
        METRICS_FILE = 'pipeline_metrics.csv'
        RUN_COUNT = '1000'  // still a string; we'll convert it later
    }

    stages {
        stage('Simulate CI/CD Runs') {
            steps {
                script {
                    // Convert RUN_COUNT to integer safely
                    def totalRuns = env.RUN_COUNT.toInteger()

                    echo "🚀 Starting ${totalRuns} simulated CI/CD pipeline runs..."

                    def metricsFile = "${env.WORKSPACE}/${env.METRICS_FILE}"

                    // Create CSV header if it doesn't exist
                    if (!fileExists(metricsFile)) {
                        writeFile file: metricsFile, text: "RunID,BuildTime,SuccessRate,FailureReason\n"
                    }

                    def random = new Random()

                    for (int i = 1; i <= totalRuns; i++) {
                        // Simulate random build time (30–600 seconds)
                        def buildTime = 30 + random.nextInt(570)

                        // Simulate success/failure (20% failure rate)
                        def success = random.nextDouble() > 0.2

                        def failureReason = success ? "" : (
                            ["UnitTestError", "IntegrationFail", "Timeout", "BuildScriptError"]
                            [random.nextInt(4)]
                        )

                        // Append metrics line
                        def csvLine = "${i},${buildTime},${success ? 1 : 0},${failureReason}\n"
                        writeFile file: metricsFile, text: csvLine, append: true
                    }

                    echo "✅ Simulation complete. Data written to ${metricsFile}"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'pipeline_metrics.csv', fingerprint: true
            echo "📊 Metrics archived for machine learning training."
        }
    }
}
