pipeline {
    agent any

    environment {
        METRICS_FILE = 'pipeline_metrics.csv'
        RUN_COUNT = '1000'
        PYTHON = 'python3'
    }

    stages {

        stage('Simulate CI/CD Runs') {
            steps {
                script {
                    def totalRuns = env.RUN_COUNT.toInteger()
                    def random = new Random()

                    echo "🚀 Starting ${totalRuns} simulated CI/CD runs..."
                    def csvData = "RunID,BuildTime,TestTime,DeployTime,Success,FailureReason\n"

                    for (int i = 1; i <= totalRuns; i++) {

                        def buildTime = (random.nextDouble() * 5 + 1).round(3)
                        def testTime = (random.nextDouble() * 4 + 0.5).round(3)
                        def deployTime = (random.nextDouble() * 3 + 0.2).round(3)

                        def success = random.nextDouble() > 0.2
                        def failureReason = success ? "" : (
                            ["UnitTestError", "IntegrationFail", "Timeout", "BuildScriptError"]
                            [random.nextInt(4)]
                        )

                        csvData += "${i},${buildTime},${testTime},${deployTime},${success ? 1 : 0},${failureReason}\n"
                    }

                    writeFile file: env.METRICS_FILE, text: csvData
                    echo "✅ Generated ${totalRuns} simulation records."
                }
            }
        }

        stage('ML Training') {
            steps {
                script {
                    echo "📚 Training ML model using pipeline_metrics.csv ..."
                    sh """
                        ${env.PYTHON} ml/train_model.py
                    """
                }
            }
        }

        stage('Optimize Pipeline') {
            steps {
                script {
                    echo "🤖 Running ML optimizer..."
                    sh """
                        ${env.PYTHON} ml/optimize_pipeline.py
                    """
                }
            }
        }

        stage('Show Optimization Report') {
            steps {
                script {
                    echo "📘 Optimization Summary:"
                    echo readFile("optimization_report.txt")
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'pipeline_metrics.csv', fingerprint: true
            archiveArtifacts artifacts: 'optimization_report.txt'
            archiveArtifacts artifacts: 'ci_cd_model.pkl'
            echo "📦 Artifacts saved."
        }
    }
}
