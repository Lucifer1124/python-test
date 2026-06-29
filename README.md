first in Linux terminal:-
docker swarm init

docker-compose.swarm.yml:-

  version: '3.8'
  services:
    flask-app:
      # Swarm will substitute these automatically from your Jenkins environment
      image: ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_ID}
      ports:
        - "4000:4000"
      deploy:
        replicas: 3  # Keeps 3 instances running simultaneously for high availability
        update_config:
          parallelism: 1  # Updates containers one at a time
          delay: 5s       # Waits 5 seconds between updating each container
        restart_policy:
          condition: on-failure
        
updated Jenkinsfile:-


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
                echo 'Deploying application stack to Docker Swarm cluster...'
                // Deploys or updates the stack with zero downtime using the swarm configuration file
                sh "docker stack deploy -c docker-compose.swarm.yml flask-stack --with-registry-auth"
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up builder caches and logging out...'
            sh "docker builder prune -f"
            sh "docker logout"
        }
    }
}
