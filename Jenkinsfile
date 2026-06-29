pipeline {
    agent any
    environment {
        DOCKER_USER  = 'lucifer1124'
        IMAGE_NAME   = 'flask-web-app'
        IMAGE_ID     = "${env.BUILD_NUMBER}"
        DOCKER_CRED  = credentials('docker-cred') 
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
        
        stage('Kubernetes Deploy') {
            steps {
                echo 'Deploying application to Kubernetes Cluster...'
                
                // Safely bindings our Jenkins secret file to a temporary environment variable path
                withCredentials([file(credentialsId: 'k8s-config', variable: 'KUBECONFIG')]) {
                    
                    //Swap placeholder with our newly built image string dynamically
                    sh "sed -i 's|LUCIFER_IMAGE_PLACEHOLDER|${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_ID}|g' k8s-deployment.yaml"
                    
                    //Apply both configurations using our secure kubeconfig reference
                    sh "kubectl apply -f k8s-deployment.yaml --kubeconfig=\$KUBECONFIG"
                    sh "kubectl apply -f k8s-service.yaml --kubeconfig=\$KUBECONFIG"
                    
                    // Monitor the rolling update status to confirm success
                    sh "kubectl rollout status deployment/flask-web-deployment --kubeconfig=\$KUBECONFIG"
                }
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