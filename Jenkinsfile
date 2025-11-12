pipeline {
    agent any

    environment {
        METRICS_FILE = "pipeline_metrics.csv"
        BUILD_START = "${new Date().getTime()}"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                script {
                    def start = System.currentTimeMillis()
                    sh 'python3 -m venv venv'
                    sh '. venv/bin/activate && pip install -r requirements.txt || true'
                    def duration = (System.currentTimeMillis() - start) / 1000
                    writeFile file: 'install_time.txt', text: "${duration}"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def start = System.currentTimeMillis()
                    def result = (new Random().nextInt(100) < 85) ? 0 : 1 // 15% failure chance
                    sh "sleep 2" // simulate test duration
                    def duration = (System.currentTimeMillis() - start) / 1000
                    writeFile file: 'test_time.txt', text: "${duration}"
                    writeFile file: 'test_result.txt', text: "${result}"
                    if (result != 0) {
                        error("Tests failed (simulated)")
                    }
                }
            }
        }

        stage('Build Simulation') {
            steps {
                script {
                    def start = System.currentTimeMillis()
                    sh 'sleep 3'
                    def duration = (System.currentTimeMillis() - start) / 1000
                    writeFile file: 'build_time.txt', text: "${duration}"
                }
            }
        }

        stage('Deploy Simulation') {
            steps {
                script {
                    def start = System.currentTimeMillis()
                    sh 'sleep 2'
                    def duration = (System.currentTimeMillis() - start) / 1000
                    writeFile file: 'deploy_time.txt', text: "${duration}"
                }
            }
        }
    }

    post {
        always {
            script {
                // Helper to safely read files (returns "0" if missing)
                def safeRead = { filename ->
                    return fileExists(filename) ? readFile(filename).trim() : "0"
                }

                // Read stage metrics
                def install_time = safeRead('install_time.txt')
                def test_time = safeRead('test_time.txt')
                def test_result = safeRead('test_result.txt')
                def build_time = safeRead('build_time.txt')
                def deploy_time = safeRead('deploy_time.txt')

                // Compute total pipeline time
                def total_time = (System.currentTimeMillis() - BUILD_START.toLong()) / 1000
                def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")

                // Line to append to CSV
                def line = "${timestamp},${install_time},${test_time},${test_result},${build_time},${deploy_time},${total_time}\n"

                // Create CSV with headers if it doesn't exist
                if (!fileExists(METRICS_FILE)) {
                    writeFile file: METRICS_FILE, text: "timestamp,install_time,test_time,test_result,build_time,deploy_time,total_time\n"
                }

                // ✅ Append directly to metrics file
                def metricsFile = new File(METRICS_FILE)
                metricsFile.append(line)
                println "✅ Metrics appended to ${METRICS_FILE}"

                // Save metrics as a build artifact
                archiveArtifacts artifacts: "${METRICS_FILE}", fingerprint: true
            }
        }

        success {
            echo '✅ Pipeline completed successfully!'
        }

        failure {
            echo '❌ Pipeline failed (simulated or real)!'
        }
    }
}
