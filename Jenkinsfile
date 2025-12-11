pipeline {
    agent any

    environment {
        FLASK_APP = 'app.py'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Siva023-cpu/login.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                bat """
                python -m venv venv
                call venv\\Scripts\\activate
                pip install -r requirements.txt
                """
            }
        }

        stage('Security Scan (Bandit)') {
            steps {
                bat """
                call venv\\Scripts\\activate
                bandit -r . -f json -o bandit-report.json || exit /b 0
                """
            }
        }

        stage('Test') {
            steps {
                bat "echo Running tests..."
            }
        }

        stage('Run Flask App') {
            steps {
                bat """
                call venv\\Scripts\\activate
                flask run --host=0.0.0.0 --port=5000
                """
            }
        }
    }
}
