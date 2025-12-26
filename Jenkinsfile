pipeline {
    agent any

    environment {
        BACKEND_IMAGE  = "my-ci-cd-backend"
        FRONTEND_IMAGE = "my-ci-cd-frontend"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout Source Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Image') {
            steps {
                echo "Building Backend Docker Image..."
                sh '''
                docker build \
                  -t ${BACKEND_IMAGE}:latest \
                  ./backend
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                echo "Building Frontend Docker Image..."
                sh '''
                docker build \
                  -f frontend/myapp/Dockerfile \
                  -t ${FRONTEND_IMAGE}:latest \
                  frontend/myapp
                '''
            }
        }
    }

    post {
        success {
            echo "✅ CI pipeline completed successfully!"
            sh 'docker images | grep my-ci-cd || true'
        }

        failure {
            echo "❌ CI pipeline failed!"
        }

        always {
            echo "🧹 CI run finished"
        }
    }
}
