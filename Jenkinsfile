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
                    def metricsFile = new File("${env.WORKSPACE}/${env.METRICS_FILE}")
                    def random = new Random()

                    echo "🚀 Starting ${totalRuns} simulated CI/CD pipeline runs..."

                    // Create CSV header if file doesn't exist
                    if (!metricsFile.exists()) {
                        metricsFile.text = "RunID,BuildTime,SuccessRate,FailureReason\n"
                    }

                    for (int i = 1; i <= totalRuns; i++) {
                        def buildTime = 30 + random.nextInt(570) // seconds
                        def success = random.nextDouble() > 0.2
                        def failureReason = success ? "" : (
                            ["UnitTestError", "IntegrationFail", "Timeout", "BuildScriptError"]
                            [random.nextInt(4)]
                        )

                        // Append using Groovy file operator
                        metricsFile << "${i},${buildTime},${success ? 1 : 0},${failureReason}\n"
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
