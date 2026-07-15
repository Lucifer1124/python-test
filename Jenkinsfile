pipeline {

    agent any

    environment {
        IMAGE_NAME = "yourdockerhub/flask-app"
    }

    triggers {
        cron('H/5 * * * *')
    }

    stages {

        stage('Clone Repository') {
            steps {
                git 'git repository URL'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Docker Login & Push') {
            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }

    }
}