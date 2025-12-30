pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "kilaruvenkatesh"

        BACKEND_IMAGE  = "my-ci-cd-backend"
        FRONTEND_IMAGE = "my-ci-cd-frontend"

        DEPLOY_ENV = "prod"

        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        /* =========================
           CLEAN & CHECKOUT
        ========================== */

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

        /* =========================
           BUILD IMAGES
        ========================== */

        stage('Build Images') {
            steps {
                sh '''
                  docker build -t $BACKEND_IMAGE:$IMAGE_TAG ./backend
                  docker build -t $FRONTEND_IMAGE:$IMAGE_TAG frontend/myapp
                '''
            }
        }

        /* =========================
           DOCKER HUB LOGIN
        ========================== */

        stage('Docker Hub Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                }
            }
        }

        /* =========================
           TAG & PUSH
        ========================== */

        stage('Push Images') {
            steps {
                sh '''
                  docker tag $BACKEND_IMAGE:$IMAGE_TAG  $DOCKERHUB_USER/$BACKEND_IMAGE:$IMAGE_TAG
                  docker tag $FRONTEND_IMAGE:$IMAGE_TAG $DOCKERHUB_USER/$FRONTEND_IMAGE:$IMAGE_TAG

                  docker push $DOCKERHUB_USER/$BACKEND_IMAGE:$IMAGE_TAG
                  docker push $DOCKERHUB_USER/$FRONTEND_IMAGE:$IMAGE_TAG
                '''
            }
        }

        /* =========================
           DEPLOY
        ========================== */

        stage('Deploy Application') {
            steps {
                sh '''
                  export IMAGE_TAG=$IMAGE_TAG
                  cd deploy/$DEPLOY_ENV
                  docker compose down
                  docker compose up -d
                '''
            }
        }

        /* =========================
           HEALTH CHECK
        ========================== */

        stage('Health Check') {
            steps {
                sh '''
                  sleep 10
                  curl -f http://localhost:7000/health
                '''
            }
        }
    }

    post {

        success {
            echo "Deployment SUCCESS with version ${IMAGE_TAG}"
        }

        failure {
            echo "Deployment FAILED — Rolling back!"

            sh '''
              PREVIOUS_TAG=$((IMAGE_TAG - 1)) || exit 0

              export IMAGE_TAG=$PREVIOUS_TAG
              cd deploy/$DEPLOY_ENV

              docker compose down
              docker compose up -d
            '''
        }
    }
}
