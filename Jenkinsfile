pipeline {
    agent any

    parameters {
        string(name: 'RUN_COUNT', defaultValue: '100', description: 'How many simulations to run (e.g. 100 or 1000)')
    }

    stages {
        stage('Run Multiple Simulations') {
            steps {
                script {
                    def count = params.RUN_COUNT.toInteger()
                    echo "Starting ${count} simulated pipeline runs..."

                    for (int i = 1; i <= count; i++) {
                        echo "===== Simulation Run #${i} ====="
                        // Trigger your main CI/CD simulation pipeline
                        build job: 'tkti', wait: true
                        sleep(time: 3, unit: 'SECONDS') // slight pause between runs
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Completed ${params.RUN_COUNT} simulated runs!"
        }
        failure {
            echo "❌ Simulation loop failed midway!"
        }
    }
}
