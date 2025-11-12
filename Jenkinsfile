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
                    sh '. venv/bin/activate && pip install -r requirements.txt || true'  // allow simulated failure
                    def duration = (System.currentTimeMillis() - start) / 1000
                    writeFile file: 'install_time.txt', text: "${duration}"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    def start = System.currentTimeMillis()
                    // simulate test success or random failure
                    def result = (new Random().nextInt(100) < 85) ? 0 : 1
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
                def install_time = readFile('install_time.txt').trim()
                def test_time = readFile('test_time.txt').trim()
                def test_result = readFile('test_result.txt').trim()
                def build_time = readFile('build_time.txt').trim()
                def deploy_time = readFile('deploy_time.txt').trim()
                def total_time = (System.currentTimeMillis() - BUILD_START.toLong()) / 1000
                def timestamp = new Date().format("yyyy-MM-dd HH:mm:ss")

                def line = "${timestamp},${install_time},${test_time},${test_result},${build_time},${deploy_time},${total_time}\n"
                if (!fileExists(METRICS_FILE)) {
                    writeFile file: METRICS_FILE, text: "timestamp,install_time,test_time,test_result,build_time,deploy_time,total_time\n"
                }
                writeFile file: 'append_metrics.groovy', text: "new File('${METRICS_FILE}').append('${line}')"
                sh 'groovy append_metrics.groovy'
                archiveArtifacts artifacts: "${METRICS_FILE}", fingerprint: true
            }
        }

        success {
            echo '✅ Pipeline completed successfully!'
        }

        failure {
            echo '❌ Pipeline failed!'
        }
    }
}
