// Licensed Materials - Property of IBM
//
// ????-??? Copyright IBM Corp. 2020 All Rights Reserved.
//
// US Government Users Restricted Rights - Use, duplication or
// disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

pipeline {
    agent {
        node {
            label 'master'
            customWorkspace "workspace/clai/${env.BRANCH_NAME}/${env.BUILD_ID}"
        }
    }
    
    environment {
        RANDOM_NAME=sh(
            script: "cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1",
            returnStdout: true
        ).trim()
        IMAGE_NAME="clai_test_${env.RANDOM_NAME}_${env.BUILD_ID}"
        CONTAINER_BASE_DIR="/root/.clai"
        CONTAINER_NAME="CLAI_test_${env.BRANCH_NAME}_${env.BUILD_ID}"
    }
    
    stages {
        stage('begin') {
            steps {
                sh """
                    sudo CLAI_DOCKER_IMAGE_NAME=${env.IMAGE_NAME} \
                         ${env.WORKSPACE}/BuildDockerImage.sh
                    sudo CLAI_DOCKER_IMAGE_NAME=${env.IMAGE_NAME} \
                         CLAI_BASEDIR=${env.WORKSPACE} \
                         ${env.WORKSPACE}/RunDockerImage.sh
                """
            }
        }
        
        //stage ('test') {
        //    steps {
                // Get the image ID
        //        IMAGE_ID = sh (
        //            script: "sudo docker image ls -q ${env.IMAGE_NAME}",
        //            returnStdout: true
        //        ).trim()
        //        echo "Image ID: ${IMAGE_ID}"
                
                // Determine which port the container is running on
                
                // SSH into the image and run pytest
        //    }
        //}
    }
    post {
        success {
            echo 'Do something when it is successful'
        }
        failure {
            echo 'Do something when it is failed'
            //script{
            //    if (env.IMAGE_ID != '') {
            //        if (env.CONTAINER_ID != '') {
            //            sh"sudo docker container stop ${env.CONTAINER_ID}"
            //            sh"sudo docker container rm ${env.CONTAINER_ID}"
            //        }
            //        sh"sudo docker image rm ${env.IMAGE_ID}"
            //    }
            //}
        }
    }
}