pipeline {
    agent any

    environment {
        // Docker Hub
        DOCKERHUB_USER = "kilaruvenkatesh"
        BACKEND_IMAGE  = "my-ci-cd-backend"
        FRONTEND_IMAGE = "my-ci-cd-frontend"

        // Environment (dev / staging / prod)
        DEPLOY_ENV = "prod"

        // Versioning
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        /* =========================
           CLEAN & CHECKOUT
        ========================== */
        stage('Clean Workspace') {
            steps {
                echo " Cleaning workspace"
                deleteDir()
            }
        }

        stage('Checkout Source Code') {
            steps {
                echo " Checking out source code"
                checkout scm
            }
        }

        /* =========================
           BUILD IMAGES
        ========================== */
        stage('Build Docker Images') {
            steps {
                echo " Building Docker images"
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
                echo "Logging into Docker Hub"
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
        stage('Push Images to Docker Hub') {
            steps {
                echo " Pushing images to Docker Hub"
                sh '''
                  docker tag $BACKEND_IMAGE:$IMAGE_TAG  $DOCKERHUB_USER/$BACKEND_IMAGE:$IMAGE_TAG
                  docker tag $FRONTEND_IMAGE:$IMAGE_TAG $DOCKERHUB_USER/$FRONTEND_IMAGE:$IMAGE_TAG

                  docker push $DOCKERHUB_USER/$BACKEND_IMAGE:$IMAGE_TAG
                  docker push $DOCKERHUB_USER/$FRONTEND_IMAGE:$IMAGE_TAG
                '''
            }
        }

        /* =========================
           MANUAL APPROVAL
        ========================== */
        stage('Approve Production Deploy') {
            steps {
                input message: " Approve deployment to PRODUCTION?",
                      ok: "Deploy"
            }
        }

        /* =========================
           DEPLOY
        ========================== */
        stage('Deploy Application') {
            steps {
                echo " Deploying to ${DEPLOY_ENV}"
                sh '''
                  export IMAGE_TAG=$IMAGE_TAG
                  cd deploy/$DEPLOY_ENV

                  docker-compose down
                  docker-compose pull
                  docker-compose up -d
                '''
            }
        }

        /* =========================
           HEALTH CHECK (CORRECT)
        ========================== */
        stage('Health Check') {
            steps {
                echo " Performing health check"
                sh '''
                  for i in {1..10}; do
                    docker run --rm --network prod_app-network curlimages/curl \
                      curl -f http://backend-prod:5000/health && exit 0
                    echo "Waiting for backend..."
                    sleep 5
                  done
                  exit 1
                '''
            }
        }
    }

    /* =========================
       POST ACTIONS (ROLLBACK)
    ========================== */
    post {

        success {
            echo " Deployment SUCCESS — Version ${IMAGE_TAG}"
            sh '''
              echo $IMAGE_TAG > deploy/prod/last_successful_tag.txt
            '''
        }

        failure {
            echo " Deployment FAILED — Rolling back!"

            sh '''
              if [ -f deploy/prod/last_successful_tag.txt ]; then
                ROLLBACK_TAG=$(cat deploy/prod/last_successful_tag.txt)
                echo " Rolling back to version $ROLLBACK_TAG"

                export IMAGE_TAG=$ROLLBACK_TAG
                cd deploy/prod

                docker-compose down
                docker-compose pull
                docker-compose up -d
              else
                echo " No rollback version found"
              fi
            '''
        }
    }
}
