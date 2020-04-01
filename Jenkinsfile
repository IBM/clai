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
        COMMON_NAME="${env.RANDOM_NAME}_${env.BUILD_ID}"
        IMAGE_NAME="clai_tstimg_${env.COMMON_NAME}"
        //IMAGE_NAME="claiplayground"
        CONTAINER_NAME="clai_tstctr_${env.COMMON_NAME}"
        //CONTAINER_NAME="CLAIBotPlayground"
    }
    
    stages {
        stage('begin') {
            steps {
                script{
                
                    // Check the preconditions needed for this Jenkinsfile to run
                    sh"${env.WORKSPACE}/checkJenkinsPreconditions.sh"
                
                    // Does an image with the given name already exist?
                    // If not, create it.
                    IMAGE_ID = getImageID(env.IMAGE_NAME)
                    if(IMAGE_ID){
                        echo "Image ID: ${IMAGE_ID}"
                    }
                    else{
                        sh """
                            sudo DOCKER_BUILD_FLAGS='' \
                            CLAI_DOCKER_IMAGE_NAME=${env.IMAGE_NAME} \
                            CLAI_DOCKER_JENKINSBUILD='true' \
                            ${env.WORKSPACE}/BuildDockerImage.sh
                        """
                    }
                    
                    // Does a container with the given name already exist?
                    // If not, create it.
                    CONTAINER_ID = getContainerID(env.CONTAINER_NAME)
                    if(CONTAINER_ID){
                        echo "Container ID: ${CONTAINER_ID}"
                    }
                    else{
                        sh """
                            sudo CLAI_DOCKER_IMAGE_NAME=${env.IMAGE_NAME} \
                                CLAI_DOCKER_CONTAINER_NAME=${env.CONTAINER_NAME} \
                                CLAI_BASEDIR=${env.WORKSPACE} \
                                ${env.WORKSPACE}/RunDockerImage.sh
                        """
                        CONTAINER_ID = getContainerID(env.CONTAINER_NAME)
                        echo "Container ID: ${CONTAINER_ID}"
                    }
                    
                    // Get the port that the container is listening on
                    CONTAINER_IP = getContainerIP(CONTAINER_ID)
                    if(CONTAINER_IP){
                        echo "Container IP: ${CONTAINER_IP}"
                    }
                    else{
                        echo "No container ip"
                        exit 4
                    }
                    
                    echo "'begin' step complete"
                }
            }
        }
        
        stage ('test') {
            steps {
                script{

                    // Does a container with the given name already exist?
                    // If not, create it.
                    CONTAINER_ID = getContainerID(env.CONTAINER_NAME)
                    if(!CONTAINER_ID){
                        exit 2
                    }
                    
                    // Get the port that the container is listening on
                    CONTAINER_IP = getContainerIP(CONTAINER_ID)
                    if(!CONTAINER_IP){
                        exit 4
                    }
                    
                    // Launch pytest in the container
                    CMD_RC = runCommandInContainer(CONTAINER_IP, 'pytest')
                    if(CMD_RC != 0){
                        exit 8
                    }
                    
                    echo "'test' step complete"
                }
            }
        }
    }
    post {
        success {
            echo 'Build successful'
            cleanupBuild()
        }
        failure {
           echo 'Build failed!'
           cleanupBuild()
        }
    }
}

def getImageID(String imgName){
    IMAGE_ID = sh (
        script: "sudo docker image ls -q ${imgName}",
        returnStdout: true
    ).trim()
    
    return (IMAGE_ID == "") ? null : IMAGE_ID
}

def getContainerID(String ctrName){
    CONTAINER_ID = sh (
        script: "sudo docker container ls -q --filter name=${ctrName}",
        returnStdout: true
    ).trim()
    
    return (CONTAINER_ID == "") ? null : CONTAINER_ID
}

def getContainerIP(String ctrID){
    CONTAINER_IP = sh (
        script: "sudo docker container ls --filter id=${ctrID} \
                 | tail -n1 \
                 | tr -s ' ' \
                 | rev \
                 | cut -d' ' -f2 \
                 | rev \
                 | cut -d'-' -f1",
        returnStdout: true
    ).trim()
    
    return (CONTAINER_IP == "" || CONTAINER_IP == "PORTS") ? null : CONTAINER_IP
}

def runCommandInContainer(String container_ip, String command){
    CONTAINER_IP_ADDR=sh(
        script: "echo ${container_ip} | cut -d':' -f1",
        returnStdout: true
    ).trim()
    CONTAINER_PORT=sh(
        script: "echo ${container_ip} | cut -d':' -f2",
        returnStdout: true
    ).trim()
    EXIT_STATUS = sh(
        returnStatus: true,
        script: "sshpass -p Bashpass \
                 ssh -o 'StrictHostKeyChecking=no' \
                     root@${CONTAINER_IP_ADDR} \
                     -p ${CONTAINER_PORT} 'cd ./.clai ; ${command}'"
    )
    
    return EXIT_STATUS
}

def cleanupBuild(){
    CONTAINER_ID = getContainerID(env.CONTAINER_NAME)
    if(CONTAINER_ID){
        sh"""
            sudo docker container stop ${CONTAINER_ID}
            sudo docker container rm ${CONTAINER_ID}
        """
    }
    
    IMAGE_ID = getImageID(env.IMAGE_NAME)
    if(IMAGE_ID){
        sh"sudo docker image rm ${IMAGE_ID}"
    }
}
