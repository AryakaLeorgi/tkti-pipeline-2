pipeline {
    agent any

    environment {
        METRICS_FILE = 'pipeline_metrics.csv'
        RUN_COUNT = '1000'
    }

    stages {
        stage('Simulate CI/CD Runs') {
            steps {
                script {
                    def totalRuns = env.RUN_COUNT.toInteger()
                    def random = new Random()

                    echo "🚀 Starting ${totalRuns} simulated CI/CD pipeline runs..."

                    // Start with CSV header
                    def csvData = "RunID,BuildTime,TestTime,DeployTime,Success,FailureReason\n"

                    for (int i = 1; i <= totalRuns; i++) {
                        // Randomly simulate times (seconds)
                        def buildTime = (random.nextDouble() * 5 + 1).round(3)  // 1–6 seconds
                        def testTime = (random.nextDouble() * 4 + 0.5).round(3) // 0.5–4.5 sec
                        def deployTime = (random.nextDouble() * 3 + 0.2).round(3) // 0.2–3.2 sec

                        // Success or fail (20% chance of failure)
                        def success = random.nextDouble() > 0.2
                        def failureReason = success ? "" : (
                            ["UnitTestError", "IntegrationFail", "Timeout", "BuildScriptError"]
                            [random.nextInt(4)]
                        )

                        // Append data to CSV string
                        csvData += "${i},${buildTime},${testTime},${deployTime},${success ? 1 : 0},${failureReason}\n"
                    }

                    // Finally write it once
                    writeFile file: env.METRICS_FILE, text: csvData

                    echo "✅ Generated ${totalRuns} simulation records into ${env.METRICS_FILE}"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'pipeline_metrics.csv', fingerprint: true
            echo "📊 Metrics archived for ML training."
        }
    }
}
