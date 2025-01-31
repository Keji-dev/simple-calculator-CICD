pipeline {
    agent any
    
    stages {
        stage('Get Code') {
            steps {
                git url: 'https://github.com/Keji-dev/unir-helloworld.git', branch: 'feature_fix_coverage'
            }
        }

        stage('Unit Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh 'export PYTHONPATH=$(pwd) && pytest --junitxml=result-unit.xml test/unit/'
                    junit 'result-unit.xml'
                }
            }
        }

        stage('Rest Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        docker run -d -p 9090:8080 --name wiremock \
                        -v $(pwd)/test/wiremock/mappings:/home/wiremock/mappings \
                        wiremock/wiremock:latest

                        TIMEOUT=300
                        TIME_ELAPSED=0

                        until curl -s http://localhost:9090/__admin; do
                            if [ $TIME_ELAPSED -ge $TIMEOUT ]; then
                                echo "[ERROR] Unable to start WireMock. Timeout reached after $TIMEOUT seconds, stopping pipeline..."
                                exit 1
                            fi

                            echo "[INFO] Waiting for Flask to be initiated..."
                            sleep 5
                            TIME_ELAPSED=$((TIME_ELAPSED + 5))
                        done

                        echo "[OK] WireMock started"

                        # Ejecutamos Flask y realizamos las pruebas

                        export FLASK_APP=app/api.py
                        nohup flask run > flask.log 2>&1 &

                        TIMEOUT=300
                        TIME_ELAPSED=0

                        until curl -s http://localhost:5000; do
                            if [ $TIME_ELAPSED -ge $TIMEOUT ]; then
                                echo "[ERROR] Unable to start Flask. Timeout reached after $TIMEOUT seconds, stopping pipeline..."
                                exit 1
                            fi

                            echo "[INFO] Waiting for Flask to be initiated..."
                            sleep 5
                            TIME_ELAPSED=$((TIME_ELAPSED + 5))
                        done

                        echo "[OK] Flask started"

                        export PYTHONPATH=$WORKSPACE
                        pytest test/rest/api_test.py --junitxml=result-rest.xml
                    '''
                    junit 'result-rest.xml'
                }
            }             
        }

        stage('Code Coverage') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        python3 -m coverage run --branch --source=app --omit=app/__init.py,app/api.py -m pytest test/unit/
                        python3 -m coverage xml
                    '''
                    cobertura coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '100,80,90', lineCoverageTargets: '100,85,95', failUnhealthy: false, failUnstable: true
                }
            }    
        }

        stage('Static') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        python3 -m flake8 --exit-zero --format=pylint app > flake8.out
                    '''
                    recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], qualityGates: [[threshold: 8, type: 'TOTAL', unstable: true], [threshold: 10, type: 'TOTAL', unstable: false]]
                }
            }
        }

        stage('Security') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        bandit -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}] {msg}" || exit 0
                    '''
                    recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], qualityGates: [[threshold: 2, type: 'TOTAL', unstable: true], [threshold: 4, type: 'TOTAL', unstable: false]]
                }
            }
        }

        stage('Performance') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    sh '''
                        export PATH=$PATH:/opt/jmeter/bin
                        jmeter -n -t test/jmeter/flask.jmx -f -l flask.jtl
                    '''
                    perfReport sourceDataFiles: 'flask.jtl'
                }
            }
        }
    }

    post {
        always {
            sh '''
                echo "[INFO] Cleaning resources and workspace..." 
                docker stop wiremock || true
                docker rm wiremock || true
                pkill -f "flask" || true
            '''
            cleanWs()
        }
    }
}