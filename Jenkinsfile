pipeline {
    agent any

    stages {
        stage('Simulate CI/CD Pipeline Metrics') {
            steps {
                script {
                    def csvFile = "${env.WORKSPACE}/pipeline_metrics.csv"
                    def writer = new File(csvFile)
                    def random = new Random()

                    // CSV header
                    writer.write("Run,BuildTime,TestTime,DeployTime,TotalTime,Success,FailedStage,CommitSize,Developers,Timestamp\n")

                    int totalRuns = 1000
                    echo "🚀 Starting ${totalRuns} simulated CI/CD runs..."

                    for (int i = 1; i <= totalRuns; i++) {

                        // --- Simulate stage durations ---
                        def buildTime = Math.max(30,  random.nextGaussian() * 15 + 100)   // build ~100s ±15s
                        def testTime  = Math.max(10,  random.nextGaussian() * 10 + 60)    // test ~60s ±10s
                        def deployTime = Math.max(5,  random.nextGaussian() * 5 + 30)     // deploy ~30s ±5s
                        def totalTime = buildTime + testTime + deployTime

                        // --- Simulate other metadata ---
                        def commitSize = Math.max(1, (int)(random.nextGaussian() * 50 + 200)) // lines of code changed
                        def developers = Math.max(1, (int)(random.nextGaussian() * 1.5 + 3))  // number of devs working

                        // --- Simulate failures (10–15% chance) ---
                        def success = random.nextInt(100) >= 12
                        def failedStage = success ? "None" : ["Build", "Test", "Deploy"][random.nextInt(3)]

                        // Timestamp
                        def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")

                        // Write to CSV
                        writer.append("${i},${String.format('%.2f', buildTime)},${String.format('%.2f', testTime)},${String.format('%.2f', deployTime)},${String.format('%.2f', totalTime)},${success},${failedStage},${commitSize},${developers},${timestamp}\n")

                        // Progress logs
                        if (i % 100 == 0) {
                            echo "✅ Generated ${i} simulated runs..."
                        }
                    }

                    writer.close()
                    echo "🎉 Simulation complete! Metrics saved to ${csvFile}"
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'pipeline_metrics.csv', onlyIfSuccessful: false
            echo "📦 CSV file archived — you can download it from the Jenkins build artifacts."
        }
    }
}
