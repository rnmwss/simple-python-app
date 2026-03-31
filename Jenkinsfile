pipeline {
    agent any
    
    parameters {
        string(name: 'STUDENT_NAME', defaultValue: 'Иванов Иван', description: 'ФИО студента')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'production'], description: 'Среда')
    }
    
    environment {
        DOCKER_IMAGE = "rnmwws/student-app:${BUILD_NUMBER}"
        CONTAINER_NAME = "student-app-${ENVIRONMENT}"
        HOST_PORT = "${params.ENVIRONMENT == 'production' ? '80' : (params.ENVIRONMENT == 'staging' ? '8082' : '8081')}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rnmwss/simple-python-app.git', credentialsId: 'github-credentials'
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'docker-hub-credentials') {
                        def customImage = docker.build("${DOCKER_IMAGE}")
                        customImage.push()
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
                sh "docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:5000 -e STUDENT_NAME='${params.STUDENT_NAME}' ${DOCKER_IMAGE}"
            }
        }
        
        stage('Approve Production') {
            when { expression { params.ENVIRONMENT == 'production' } }
            steps {
                script {
                    env.PROD_VERSION = input(
                        message: "Подтвердите развертывание в PRODUCTION?", ok: "Да, развернуть",
                        parameters:[string(name: 'PROD_VERSION', defaultValue: "v1.0.${BUILD_NUMBER}")]
                    )
                }
            }
        }

        stage('Tag Release') {
            when { expression { params.ENVIRONMENT == 'production' } }
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-credentials', passwordVariable: 'GIT_PASS', usernameVariable: 'GIT_USER')]) {
                    sh '''
                        git config user.email "jenkins@ci.com"
                        git config user.name "Jenkins CI"
                        git tag -a "$PROD_VERSION" -m "Release $PROD_VERSION"
                        git push "https://$GIT_USER:$GIT_PASS@github.com/rnmwss/simple-python-app.git" "$PROD_VERSION"
                    '''
                }
            }
        }
    }

    post {
        success {
            emailext(
                to: 'romanginko25072006@gmail.com',
                subject: "✅ УСПЕХ: Pipeline ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: "<p>Сборка #${env.BUILD_NUMBER} успешно развернута в <b>${params.ENVIRONMENT}</b>.</p>"
            )
        }
        failure {
            emailext(
                to: 'romanginko25072006@gmail.com',
                subject: "❌ ОШИБКА: Pipeline ${env.JOB_NAME} [${env.BUILD_NUMBER}]",
                body: "<p>Сборка #${env.BUILD_NUMBER} упала. Проверьте консоль: ${env.BUILD_URL}</p>"
            )
        }
    }
}

