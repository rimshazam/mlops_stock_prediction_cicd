pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo '✅ Pulling latest code from main branch...'
                checkout scm
            }
        }

        stage('Show Project Structure') {
            steps {
                echo '✅ Displaying project structure...'
                sh 'ls -la'
                sh 'echo "Backend files:"; ls -la backend/'
                sh 'echo "Frontend files:"; ls -la frontend/'
                sh 'echo "Database files:"; ls -la database/'
            }
        }

        stage('Validate Jenkinsfile') {
            steps {
                echo '✅ Validating Jenkinsfile exists...'
                sh 'test -f Jenkinsfile && echo "Jenkinsfile found!"'
            }
        }

        stage('Validate Docker Files') {
            steps {
                echo '✅ Validating Dockerfiles...'
                sh 'test -f backend/Dockerfile && echo "Backend Dockerfile found!"'
                sh 'test -f frontend/Dockerfile && echo "Frontend Dockerfile found!"'
                sh 'test -f database/Dockerfile && echo "Database Dockerfile found!"'
                sh 'test -f docker-compose.yml && echo "Docker Compose file found!"'
            }
        }

        stage('Show Requirements') {
            steps {
                echo '✅ Showing backend requirements...'
                sh 'cat backend/requirements.txt'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo '📋 Summary:'
            echo '  - Code checked out from GitHub'
            echo '  - Project structure validated'
            echo '  - All Docker files present'
            echo '  - Ready for deployment!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for details.'
        }
    }
}
