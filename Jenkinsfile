pipeline {
    agent any
    environment {
        DOCKER_USER = 'lucifer1124'
        IMAGE_NAME  = 'flask-web-app'
        IMAGE_ID    = "${env.BUILD_NUMBER}"
        DOCKER_CRED = credentials('docker-cred') 
    }
    
    triggers {
        cron('H/5 * * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test App') {
            agent {
                docker { image 'python:3.9-slim' }
            }
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt pytest
                    pytest
                '''
            }
        }
        
        stage('Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_ID} ."
                sh "docker tag ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_ID} ${DOCKER_USER}/${IMAGE_NAME}:latest"
            }
        }
        
        stage('Docker Push') {
            steps {
                sh "echo \$DOCKER_CRED_PSW | docker login -u \$DOCKER_CRED_USR --password-stdin"
                sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_ID}"
                sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:latest"
            }
        }
        
        stage('Final run and deploy') {
            steps {
            
                sh "docker stop ${IMAGE_NAME}-container || true"
                sh "docker rm ${IMAGE_NAME}-container || true"
                sh "docker run -d --name ${IMAGE_NAME}-container -p 4000:4000 ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_ID}"
            }
        }
    }
    
    post {
        always {
            sh "docker builder prune -f"
            sh "docker logout"
        }
    }
}
