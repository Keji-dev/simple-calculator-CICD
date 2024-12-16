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
            parallel {
                stage('Wiremock Server') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                docker run -d -p 9090:8080 --name wiremock \
                                -v $(pwd)/test/wiremock/mappings:/home/wiremock/mappings \
                                wiremock/wiremock:latest

                                until curl -s http://localhost:9090/__admin; do
                                    echo "[INFO] Esperando que WireMock se inicie..."
                                    sleep 5
                                done

                                echo "[OK] WireMock está listo"
                            '''
                        }    
                    }
                }

                stage('Flask Server') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                export FLASK_APP=app/api.py
                                nohup flask run > flask.log 2>&1 &

                                until curl -s http://localhost:5000; do
                                    echo "[INFO] Esperando que Flask se inicie..."
                                    sleep 5
                                done

                                echo "[OK] Flask está listo"
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

    post {
        always {
            echo "[INFO] Limpiando recursos..."
            sh '''
                docker stop wiremock || true
                docker rm wiremock || true
                pkill -f "flask" || true
            '''
        }
    }
}
