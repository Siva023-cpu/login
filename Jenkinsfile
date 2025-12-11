pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "vasgrills"
        IMAGE_NAME = "flask-login-app"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/Siva023-cpu/login.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Security Scan (Bandit)') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                bandit -r . -f json -o bandit-report.json || echo "Bandit found issues but continuing pipeline"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat """
                docker build -t %DOCKERHUB_USER%/%IMAGE_NAME%:latest .
                """
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    bat """
                    echo %PASS% | docker login -u %USER% --password-stdin
                    """
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                bat """
                docker push %DOCKERHUB_USER%/%IMAGE_NAME%:latest
                """
            }
        }

        stage('Deploy Container') {
            steps {
                bat """
                docker rm -f flask-dev || echo already removed
                docker run -d -p 5000:5000 --name flask-dev %DOCKERHUB_USER%/%IMAGE_NAME%:latest
                """
            }
        }
    }
}

