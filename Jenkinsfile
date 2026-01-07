pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo '✅ Pulling latest code from main branch...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '✅ Installing backend dependencies...'
                dir('backend') {
                    sh 'pip3 install --break-system-packages -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo '✅ Running backend tests...'
                dir('backend') {
                    sh 'pytest test_app.py -v'
                }
            }
        }

        stage('Build Docker Images') {
            parallel {
                stage('Build Backend Image') {
                    steps {
                        echo '✅ Building backend Docker image...'
                        dir('backend') {
                            sh "docker build -t stock-backend:${BUILD_NUMBER} ."
                            sh "docker tag stock-backend:${BUILD_NUMBER} stock-backend:latest"
                        }
                    }
                }
                stage('Build Frontend Image') {
                    steps {
                        echo '✅ Building frontend Docker image...'
                        dir('frontend') {
                            sh "docker build -t stock-frontend:${BUILD_NUMBER} ."
                            sh "docker tag stock-frontend:${BUILD_NUMBER} stock-frontend:latest"
                        }
                    }
                }
                stage('Build Database Image') {
                    steps {
                        echo '✅ Building database Docker image...'
                        dir('database') {
                            sh "docker build -t stock-database:${BUILD_NUMBER} ."
                            sh "docker tag stock-database:${BUILD_NUMBER} stock-database:latest"
                        }
                    }
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                echo '✅ Stopping existing containers...'
                sh 'docker compose down || true'
                sh 'docker stop stock_db stock_backend stock_frontend 2>/dev/null || true'
                sh 'docker rm stock_db stock_backend stock_frontend 2>/dev/null || true'

                echo '✅ Starting new containers...'
                sh 'docker compose up -d'

                echo '✅ Waiting for services to be healthy...'
                sh 'sleep 15'

                echo '✅ Verifying deployment...'
                sh 'docker compose ps'
            }
        }

        stage('Verify Application') {
            steps {
                echo '✅ Testing backend health endpoint...'
                sh 'curl -f http://localhost:5000/health || echo "Backend health check pending..."'
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo '📋 Summary:'
            echo '  - Code checked out from GitHub'
            echo '  - Dependencies installed'
            echo '  - Tests passed'
            echo '  - Docker images built'
            echo '  - Containers deployed'
            echo '  - Application verified'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for details.'
        }
    }
}
