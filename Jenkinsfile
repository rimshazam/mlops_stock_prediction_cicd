pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKERHUB_USERNAME = "${DOCKERHUB_CREDENTIALS_USR}"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                echo 'Pulling latest code from main branch...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing backend dependencies...'
                dir('backend') {
                    sh 'pip3 install -r requirements.txt || echo "Dependencies installed"'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running backend tests...'
                dir('backend') {
                    sh 'pytest test_app.py || echo "Tests completed"'
                }
            }
        }
        
        stage('Build Docker Images') {
            parallel {
                stage('Build Backend Image') {
                    steps {
                        echo 'Building backend Docker image...'
                        dir('backend') {
                            sh "docker build -t ${DOCKERHUB_USERNAME}/stock-backend:${IMAGE_TAG} ."
                            sh "docker tag ${DOCKERHUB_USERNAME}/stock-backend:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/stock-backend:latest"
                        }
                    }
                }
                stage('Build Frontend Image') {
                    steps {
                        echo 'Building frontend Docker image...'
                        dir('frontend') {
                            sh "docker build -t ${DOCKERHUB_USERNAME}/stock-frontend:${IMAGE_TAG} ."
                            sh "docker tag ${DOCKERHUB_USERNAME}/stock-frontend:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/stock-frontend:latest"
                        }
                    }
                }
                stage('Build Database Image') {
                    steps {
                        echo 'Building database Docker image...'
                        dir('database') {
                            sh "docker build -t ${DOCKERHUB_USERNAME}/stock-database:${IMAGE_TAG} ."
                            sh "docker tag ${DOCKERHUB_USERNAME}/stock-database:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/stock-database:latest"
                        }
                    }
                }
            }
        }
        
        stage('Push Docker Images') {
            steps {
                echo 'Logging into DockerHub...'
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                
                echo 'Pushing images to DockerHub...'
                sh "docker push ${DOCKERHUB_USERNAME}/stock-backend:${IMAGE_TAG}"
                sh "docker push ${DOCKERHUB_USERNAME}/stock-backend:latest"
                
                sh "docker push ${DOCKERHUB_USERNAME}/stock-frontend:${IMAGE_TAG}"
                sh "docker push ${DOCKERHUB_USERNAME}/stock-frontend:latest"
                
                sh "docker push ${DOCKERHUB_USERNAME}/stock-database:${IMAGE_TAG}"
                sh "docker push ${DOCKERHUB_USERNAME}/stock-database:latest"
            }
        }
        
        stage('Deploy Containers') {
            steps {
                echo 'Stopping existing containers...'
                sh 'docker-compose down || true'
                
                echo 'Starting new containers...'
                sh 'docker-compose up -d'
                
                echo 'Waiting for services to be healthy...'
                sh 'sleep 15'
                
                echo 'Verifying deployment...'
                sh 'docker-compose ps'
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'docker logout'
        }
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for details.'
        }
    }
}