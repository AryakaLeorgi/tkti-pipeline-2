pipeline {
    agent any

    environment {
        METRICS_FILE = "pipeline_metrics.csv"
        MODEL_FILE = "ci_cd_model.pkl"
        RECOMMEND_FILE = "ml/decision.json"
    }

    stages {

        stage('Simulate CI/CD Runs') {
            steps {
                echo "🚀 Starting 1000 simulated CI/CD runs..."
                script {
                    writeFile file: METRICS_FILE, text: libraryResource('simulation/pipeline_metrics.csv')
                }
                echo "✅ Generated 1000 simulation records."
            }
        }

        stage('ML Training') {
            steps {
                echo "📚 Training ML model..."
                sh "python3 ml/train_model.py"
            }
        }

        stage('ML Optimization') {
            steps {
                echo "🤖 Running ML optimizer..."
                sh "python3 ml/optimize_pipeline.py"
            }
        }

        stage('Adaptive Build (ML Feedback Loop)') {
            steps {
                script {
                    def decision = readJSON file: RECOMMEND_FILE

                    echo "🔍 ML Decision: ${decision}"

                    if (decision.enable_cache == true) {
                        echo "⚡ Using build cache (recommended by ML)"
                        sh "echo 'Running build with cache...'"
                        sh "sleep 1"
                    } else {
                        echo "❌ Cache disabled"
                    }

                    if (decision.skip_tests == true) {
                        echo "⚡ ML recommends skipping long tests"
                    } else {
                        echo "▶ Running test normally"
                        sh "echo 'Running unit tests...'"
                        sh "sleep 1"
                    }

                    if (decision.parallel_build == true) {
                        echo "⚡ ML recommends parallel build"
                        sh "echo 'Parallel build simulation...'"
                        sh "sleep 1"
                    }
                }
            }
        }

        stage('Show Optimization Report') {
            steps {
                echo "📘 Final ML Decisions:"
                sh "cat ${RECOMMEND_FILE}"
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '*.csv'
            archiveArtifacts artifacts: '*.pkl'
            archiveArtifacts artifacts: 'ml/*.json'
            echo "📦 Artifacts saved."
        }
    }
}
