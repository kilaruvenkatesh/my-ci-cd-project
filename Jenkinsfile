pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "kilaruvenkatesh"

        BACKEND_IMAGE  = "my-ci-cd-backend"
        FRONTEND_IMAGE = "my-ci-cd-frontend"

        // Change this to dev / staging / prod when needed
        DEPLOY_ENV = "prod"
    }

    stages {

        /* =========================
           CLEAN & CHECKOUT
        ========================== */

        stage('Clean Workspace') {
            steps {
                echo ' Cleaning Jenkins workspace...'
                deleteDir()
            }
        }

        stage('Checkout Source Code') {
            steps {
                echo ' Checking out source code...'
                checkout scm
            }
        }

        /* =========================
           BUILD IMAGES
        ========================== */

        stage('Build Backend Image') {
            steps {
                echo ' Building Backend Docker Image...'
                sh 'docker build -t $BACKEND_IMAGE:latest ./backend'
            }
        }

        stage('Build Frontend Image') {
            steps {
                echo ' Building Frontend Docker Image...'
                sh 'docker build -t $FRONTEND_IMAGE:latest frontend/myapp'
            }
        }

        /* =========================
           DOCKER HUB LOGIN
        ========================== */

        stage('Docker Hub Login') {
            steps {
                echo ' Logging into Docker Hub...'
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

        /* =========================
           TAG & PUSH
        ========================== */

        stage('Tag Images') {
            steps {
                echo ' Tagging Docker images...'
                sh '''
                    docker tag $BACKEND_IMAGE:latest  $DOCKERHUB_USER/$BACKEND_IMAGE:latest
                    docker tag $FRONTEND_IMAGE:latest $DOCKERHUB_USER/$FRONTEND_IMAGE:latest
                '''
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                echo ' Pushing images to Docker Hub...'
                sh '''
                    docker push $DOCKERHUB_USER/$BACKEND_IMAGE:latest
                    docker push $DOCKERHUB_USER/$FRONTEND_IMAGE:latest
                '''
            }
        }

        /* =========================
           DEPLOY (DEV / STAGING / PROD)
        ========================== */

        stage('Deploy Application') {
            steps {
                echo " Deploying to ${DEPLOY_ENV} environment..."
                sh '''
                    cd deploy/$DEPLOY_ENV
                    docker compose down
                    docker compose pull
                    docker compose up -d
                '''
            }
        }

        /* =========================
           HEALTH CHECK
        ========================== */

        stage('Health Check') {
            steps {
                echo ' Performing health check...'
                sh '''
                    sleep 10
                    curl -f http://localhost:7000/health
                '''
            }
        }
    }

    post {
        success {
            echo ' CI/CD pipeline completed successfully!'
        }
        failure {
            echo ' CI/CD pipeline failed!'
        }
    }
}
