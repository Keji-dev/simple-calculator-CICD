pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                sh 'echo "Hello World"'
                sh 'rm -rf unir-helloworld'
                sh 'git clone -b dev https://github.com/Keji-dev/unir-helloworld.git'
                sh 'ls -la unir-helloworld'
                sh 'echo "Working directory: $WORKSPACE"'
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Build step completed"'
            }
        }
    }
}