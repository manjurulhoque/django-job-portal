#!groovy

// node {
//
//     try {
//         stage 'Checkout'
//             checkout scm
//
//             sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
//             def lastChanges = readFile('GIT_CHANGES')
//             //slackSend color: "warning", message: "Started `${env.JOB_NAME}#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges}"
//
//         stage 'Deploy'
//             sh './deployment/deploy_prod.sh'
//
//         stage 'Publish results'
//             echo "Deployment successful"
//             //slackSend color: "good", message: "Build successful: `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
//     }
//
//     catch (err) {
//         echo "Error found"
//         //slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
//
//         throw err
//     }
//
// }

// pipeline {
//     agent any
//
//     stages {
//         stage('Checkout') {
//             steps {
//                 git 'https://github.com/manjurulhoque/django-job-portal.git'
//             }
//         }
//
//         stage('Build and Deploy') {
//             steps {
//                 script {
//                     // navigate into the correct directory
//                     sh 'cd projects/django/job-portal/'
//
//                     // build and run docker-compose
//                     sh 'docker-compose -f docker-compose.prod.yml up --build -d'
//                 }
//             }
//         }
//     }
// }

node {

    try {
        stage 'Checkout'
            checkout scm

            sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
            def lastChanges = readFile('GIT_CHANGES')
            //slackSend color: "warning", message: "Started `${env.JOB_NAME}#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges}"

        stage 'Deploy'
            // sh 'cd projects/django/job-portal/'
            sh './deployment/jenkins_deploy_prod_docker.sh'

        stage 'Publish results'
            echo "Deployment successful"
            //slackSend color: "good", message: "Build successful: `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
    }

    catch (err) {
        echo "Error found"
        //slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"

        throw err
    }

}

