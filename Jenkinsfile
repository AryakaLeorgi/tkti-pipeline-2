pipeline {
    agent any

    stages {
        stage('Simulate CI/CD Pipeline Metrics') {
            steps {
                script {
                    def csvFile = "${env.WORKSPACE}/pipeline_metrics.csv"
                    def random = new Random()
                    def totalRuns = 1000

                    // CSV header
                    def header = "Run,BuildTime,TestTime,DeployTime,TotalTime,Success,FailedStage,CommitSize,Developers,Timestamp\n"
                    writeFile file: csvFile, text: header

                    echo "🚀 Starting ${totalRuns} simulated CI/CD runs..."

                    def allLines = new StringBuilder()

                    for (int i = 1; i <= totalRuns; i++) {
                        // --- Simulate times with Gaussian randomness ---
                        def buildTime = Math.max(30,  random.nextGaussian() * 15 + 100)
                        def testTime  = Math.max(10,  random.nextGaussian() * 10 + 60)
                        def deployTime = Math.max(5,  random.nextGaussian() * 5 + 30)
                        def totalTime = buildTime + testTime + deployTime

                        // --- Metadata ---
                        def commitSize = Math.max(1, (int)(random.nextGaussian() * 50 + 200))
                        def developers = Math.max(1, (int)(random.nextGaussian() * 1.5 + 3))

                        // --- Failures (15% chance) ---
                        def success = random.nextInt(100) >= 15
                        def failedStage = success ? "None" : ["Build", "Test", "Deploy"][random.nextInt(3)]

                        // --- Timestamp ---
                        def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")

                        // --- Construct CSV line ---
                        def line = "${i},${String.format('%.2f', buildTime)},${String.format('%.2f', testTime)},${String.format('%.2f', deployTime)},${String.format('%.2f', totalTime)},${success},${failedStage},${commitSize},${developers},${timestamp}\n"
                        allLines.append(line)

                        if (i % 100 == 0) {
                            echo "✅ Generated ${i} simulated runs..."
                        }
                    }

                    // Save all data in one go
                    writeFile file: csvFile, text: header + allLines.toString()
                    echo "🎉 Simulation complete! Metrics saved to ${csvFile}"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'pipeline_metrics.csv', onlyIfSuccessful: false
            echo "📦 CSV file archived — you can download it from Jenkins build artifacts."
        }
    }
}
