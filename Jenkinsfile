pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Esto es una etapa Build de ejemplo'
                sh 'ls -la'
                sh 'echo $WORKSPACE'
            }
        }
        
        stage('Services') {
            stages {
                stage('Wiremock Server') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                docker run -d -p 9090:8080 --name wiremock \
                                -v $(pwd)/test/wiremock/mappings:/home/wiremock/mappings \
                                wiremock/wiremock:latest
                            '''
                        }    
                    }
                }

                stage('Flask Server') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                export FLASK_APP=app/api.py
                                nohup flask run &
                            '''    
                        }
                    }
                }
            }
        }

        stage('Tests') {
            parallel {
                stage('Unit') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh 'export PYTHONPATH=$(pwd) && pytest --junitxml=result-unit.xml test/unit/'
                        }
                    }
                }
                
                stage('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                export PYTHONPATH=$WORKSPACE
                                pytest test/rest/api_test.py --junitxml=result-rest.xml
                            '''
                        }
                    }
                }
            }    
        }
        
        stage('Results') {
            steps {
                junit 'result*.xml'
            }
        }
    }
}
