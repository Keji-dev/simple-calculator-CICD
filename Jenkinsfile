pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                sh 'echo "Hello World"'
                sh 'git clone https://github.com/anieto-unir/helloworld.git'
                sh 'ls -la'
                sh 'echo "Working directory: $WORKSPACE"'
            }
        }

        stage('Build') {

        }
    }
}