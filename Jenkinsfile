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
    }
    
    stages {
        stage('begin') {
            steps {
                script{
                
                    // Does an image with the given name already exist?
                    // If not, create it.
                    IMAGE_ID = getImageID(env.IMAGE_NAME)
                    if(!IMAGE_ID){
                        sh """
                            sudo DOCKER_BUILD_FLAGS='' \
                            CLAI_DOCKER_IMAGE_NAME=${env.IMAGE_NAME} \
                            CLAI_DOCKER_JENKINSBUILD='true' \
                            ${env.WORKSPACE}/BuildDockerImage.sh
                        """
                        echo "Image ID: ${IMAGE_ID}"
                    }
                    
                    echo "'begin' step complete"
                }
            }
        }
        
        stage ('test') {
            steps {
                script{
                    CONTAINER_NAME = sh(
                        script: "echo ${env.IMAGE_NAME} | sed -e 's/tstimg/ctrimg/g'",
                        returnStdout: true,
                        encoding: 'UTF-8'
                    ).trim()
                    
                    TEST_OUTPUT = sh(
                        script: "sudo CLAI_DOCKER_IMAGE_NAME=${env.IMAGE_NAME} \
                                      CLAI_DOCKER_CONTAINER_NAME=${CONTAINER_NAME} \
                                      CLAI_BASEDIR=${env.WORKSPACE} \
                                      CLAI_DOCKER_JENKINSBUILD='true' \
                                      CLAI_DOCKER_OUTPUT='pytest.out' \
                                      ${env.WORKSPACE}/RunDockerImage.sh",
                        returnStdout: true,
                        encoding: 'UTF-8'
                    ).trim()
                    
                    CONTAINER_ID = getContainerID(CONTAINER_NAME)
                    
                    //sh "echo ${TEST_OUTPUT}"
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
    
    RTN_VLU = (IMAGE_ID == "") ? null : IMAGE_ID
    echo "getImageID(${imgName}) returns: ${RTN_VLU}"
    return RTN_VLU
}

def getContainerID(String ctrName){
    CONTAINER_ID = sh (
        script: "sudo docker container ls -q --filter name=${ctrName}",
        returnStdout: true
    ).trim()
    
    RTN_VLU = (CONTAINER_ID == "") ? null : CONTAINER_ID
    echo "getContainerID(${ctrName}) returns: ${RTN_VLU}"
    return RTN_VLU
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