pipeline {
    agent any

    environment {
        METRICS_FILE = "metrics.csv"
        SIMULATIONS = 1000 // You can change this to 100 for faster testing
    }

    stages {
        stage('Simulate CI/CD Runs') {
            steps {
                script {
                    def random = new Random()

                    // If metrics file doesn't exist, write header
                    if (!fileExists(METRICS_FILE)) {
                        writeFile file: METRICS_FILE, text: "timestamp,install_time,build_time,test_time,deploy_time,total_time,test_result\n"
                    }

                    echo "🚀 Starting ${SIMULATIONS} simulated CI/CD pipeline runs..."

                    for (int i = 1; i <= SIMULATIONS; i++) {
                        echo "===== Simulation Run #${i} ====="

                        // Randomize stage durations (seconds)
                        def install_time = (1 + random.nextDouble() * 8).round(3)
                        def build_time = (2 + random.nextDouble() * 10).round(3)
                        def test_time = (1 + random.nextDouble() * 12).round(3)
                        def deploy_time = (0.5 + random.nextDouble() * 5).round(3)

                        // Random failure chance (e.g. 15%)
                        def test_result = random.nextDouble() < 0.15 ? 0 : 1

                        // If failed, maybe deployment is skipped
                        if (test_result == 0) {
                            deploy_time = 0
                        }

                        // Compute total time
                        def total_time = (install_time + build_time + test_time + deploy_time).round(3)
                        def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")

                        // Build a CSV line
                        def line = "${timestamp},${install_time},${build_time},${test_time},${deploy_time},${total_time},${test_result}\n"

                        // Append to CSV
                        def metricsFile = new File(METRICS_FILE)
                        metricsFile.append(line)
                    }

                    echo "✅ Simulation complete. Results saved to ${METRICS_FILE}"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'metrics.csv', fingerprint: true
            echo "📊 Metrics archived for machine learning training."
        }
    }
}
