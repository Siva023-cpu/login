pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Building Flask App"'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "Running Tests"'
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo "Deploying App"'
            }
        }
    }
}
