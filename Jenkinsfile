pipeline {
    agent any

    stages {
        stage('Random Failure Simulation') {
            steps {
                script {
                    def failures = [
                        {
                            echo "Simulating: Missing dependency"
                            sh 'npm install this-package-does-not-exist'
                        },
                        {
                            echo "Simulating: Syntax error in JS file"
                            writeFile file: 'src/broken.js', text: 'console.log("broken"'
                            sh 'node src/broken.js'
                        },
                        {
                            echo "Simulating: Test failure"
                            sh '''
                                echo "test('fail', () => { throw new Error(\\"random test fail\\") })" > random.test.js
                                npm test
                            '''
                        },
                        {
                            echo "Simulating: Build command crash"
                            sh 'exit 2'
                        },
                        {
                            echo "Simulating: Network failure"
                            sh 'curl http://this.does.not.exist.abc'
                        },
                        {
                            echo "Simulating: Permission denied"
                            sh '''
                                touch protected.txt
                                chmod -r protected.txt
                                cat protected.txt
                            '''
                        },
                        {
                            echo "Simulating: Git checkout fail"
                            sh 'git clone https://github.com/this/does-not-exist.git'
                        }
                    ]

                    def randomFailure = failures[new Random().nextInt(failures.size())]
                    randomFailure()
                }
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed randomly — explain-error plugin should now analyze this failure."
        }
    }
}
