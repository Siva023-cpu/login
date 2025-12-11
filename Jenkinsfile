
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/Siva023-cpu/login.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                bat """
                python -m venv venv
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Security Scan (Bandit)') {
            steps {
                bat """
                call venv\\Scripts\\activate
                bandit -r . -f json -o bandit-report.json || true
                """
            }
        }


        stage('Test') {
            steps {
                bat """
                echo Running tests...
                """
            }
        }

        stage('Run Flask App') {
            steps {
                bat """
                call venv\\Scripts\\activate
                set FLASK_APP=app.py
                flask run
                """
            }
        }
    }
}
