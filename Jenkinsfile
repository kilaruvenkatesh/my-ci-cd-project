pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "kilaruvenkatesh"
        BACKEND_IMAGE  = "my-ci-cd-backend"
        FRONTEND_IMAGE = "my-ci-cd-frontend"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                echo 'Cleaning Jenkins workspace...'
                deleteDir()
            }
        }

        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                sh 'docker build -t $BACKEND_IMAGE:latest ./backend'
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh 'docker build -t $FRONTEND_IMAGE:latest frontend/myapp'
            }
        }

        stage('Docker Hub Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Tag Images') {
            steps {
                sh '''
                    docker tag $BACKEND_IMAGE:latest $DOCKERHUB_USER/$BACKEND_IMAGE:latest
                    docker tag $FRONTEND_IMAGE:latest $DOCKERHUB_USER/$FRONTEND_IMAGE:latest
                '''
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                sh '''
                    docker push $DOCKERHUB_USER/$BACKEND_IMAGE:latest
                    docker push $DOCKERHUB_USER/$FRONTEND_IMAGE:latest
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Images pushed successfully to Docker Hub!'
        }
        failure {
            echo '❌ CI pipeline failed'
        }
    }
}
