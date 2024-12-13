pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'dev', url: 'https://github.com/Keji-dev/unir-helloworld.git'
            }
        }
        
        stage('Build') {
            steps {
                echo 'NO HAY NADA QUE COMPILAR'
                sh 'ls -la'
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

                stage('Wiremock Start Up') {
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
                
                stage('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh '''
                                export FLASK_APP=app/api.py
                                nohup flask run &

                                until curl -s http://localhost:5000; do
                                    echo "[INFO] Esperando que Flask se inicie..."
                                    sleep 5
                                done
                                echo "[OK] Flask está listo"

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
                junit 'result-unit.xml'
                junit 'result-rest.xml'
            }
        }
    }

    post {
        always {
            echo "[INFO] Cerrando contenedor WireMock..."
            sh 'docker stop wiremock || true'
            sh 'docker rm wiremock || true'
        }
    }
}
