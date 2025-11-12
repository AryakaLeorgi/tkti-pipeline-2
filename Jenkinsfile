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
                    // Simulate random install time between 2–10 seconds
                    def installTime = 2 + new Random().nextInt(8)
                    sh "sleep ${installTime}"
                    
                    // Simulate random chance of slow dependency
                    if (new Random().nextInt(100) < 10) { // 10% chance
                        sh "sleep 3" // extra slowdown
                        echo "⚠️ Simulated slow dependency download!"
                    }

                    writeFile file: 'install_time.txt', text: "${installTime}"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def start = System.currentTimeMillis()

                    // Random test duration between 1–5 sec
                    def testTime = 1 + new Random().nextInt(5)
                    sh "sleep ${testTime}"

                    // Simulate 20% failure chance
                    def result = (new Random().nextInt(100) < 80) ? 0 : 1
                    if (result != 0) {
                        echo "❌ Simulated test failure!"
                    }

                    writeFile file: 'test_time.txt', text: "${testTime}"
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
                    def buildTime = 2 + new Random().nextInt(6)
                    sh "sleep ${buildTime}"

                    // Random slowdown
                    if (new Random().nextInt(100) < 15) {
                        buildTime += 3
                        echo "⚙️ Simulated build cache miss!"
                    }

                    writeFile file: 'build_time.txt', text: "${buildTime}"
                }
            }
        }

        stage('Deploy Simulation') {
            steps {
                script {
                    def start = System.currentTimeMillis()
                    def deployTime = 1 + new Random().nextInt(5)
                    sh "sleep ${deployTime}"

                    // Simulate 10% chance of deployment issue
                    if (new Random().nextInt(100) < 10) {
                        deployTime += 5
                        echo "🚨 Simulated deployment slowdown!"
                    }

                    writeFile file: 'deploy_time.txt', text: "${deployTime}"
                }
            }
        }
    }

    post {
        always {
            script {
                def safeRead = { filename ->
                    return fileExists(filename) ? readFile(filename).trim() : "0"
                }

                def install_time = safeRead('install_time.txt')
                def test_time = safeRead('test_time.txt')
                def test_result = safeRead('test_result.txt')
                def build_time = safeRead('build_time.txt')
                def deploy_time = safeRead('deploy_time.txt')
                def total_time = (System.currentTimeMillis() - BUILD_START.toLong()) / 1000
                def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")

                def line = "${timestamp},${install_time},${test_time},${test_result},${build_time},${deploy_time},${total_time}\n"

                // Append safely without sandbox issues
                if (fileExists(METRICS_FILE)) {
                    def current = readFile(METRICS_FILE)
                    writeFile file: METRICS_FILE, text: current + line
                } else {
                    writeFile file: METRICS_FILE, text: "timestamp,install_time,test_time,test_result,build_time,deploy_time,total_time\n" + line
                }

                echo "✅ Metrics appended safely to ${METRICS_FILE}"

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
