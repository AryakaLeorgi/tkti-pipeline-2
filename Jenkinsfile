pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Simulation Build') {
            steps {
                sh """
                    python simulation/run_simulation.py --output pipeline_metrics.csv
                """
            }
            post {
                success {
                    archiveArtifacts artifacts: 'pipeline_metrics.csv', fingerprint: true
                }
            }
        }

        stage('Evaluate Pipeline Metrics with ML') {
            steps {
                sh """
                    python ml/evaluate_pipeline.py \
                        --input pipeline_metrics.csv \
                        --model ml/model.pkl \
                        --output ml/evaluation.json
                """
            }
            post {
                success {
                    archiveArtifacts artifacts: 'ml/evaluation.json', fingerprint: true
                }
            }
        }

        stage('Decision: Retrain or Not') {
            steps {
                script {
                    def eval = readJSON file: "ml/evaluation.json"
                    echo "Performance Score: ${eval.performance_score}"

                    if (eval.retrain_needed == true) {
                        echo "⚠ Model needs retraining!"
                        env.NEED_RETRAIN = "yes"
                    } else {
                        echo "Model still good — skipping retraining."
                        env.NEED_RETRAIN = "no"
                    }
                }
            }
        }

        stage('Retrain Model') {
            when {
                environment name: 'NEED_RETRAIN', value: 'yes'
            }
            steps {
                sh """
                    python ml/train_model.py \
                        --data pipeline_metrics.csv \
                        --output ml/model.pkl
                """
            }
            post {
                success {
                    archiveArtifacts artifacts: 'ml/model.pkl', fingerprint: true
                }
            }
        }
    }
}
