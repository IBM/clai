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
    
    options {
        ansiColor('css')
    }
    
    environment {
        RANDOM_NAME=sh(
            script: "cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 8 | head -n 1",
            returnStdout: true
        ).trim()
        COMMON_NAME="${env.RANDOM_NAME}_${env.BUILD_ID}"
        IMAGE_NAME="clai_tstimg_${env.COMMON_NAME}"
        TEST_OUTPUT_FILENAME="pytest.out"
        OUTFILE_PATH="${env.WORKSPACE}/${env.TEST_OUTPUT_FILENAME}"
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
                    CONTAINER_NAME = getContainerName(env.IMAGE_NAME)
                    sh """
                        sudo CLAI_DOCKER_IMAGE_NAME=${env.IMAGE_NAME} \
                             CLAI_DOCKER_CONTAINER_NAME=${CONTAINER_NAME} \
                             CLAI_BASEDIR=${env.WORKSPACE} \
                             CLAI_DOCKER_JENKINSBUILD='true' \
                             CLAI_DOCKER_OUTPUT='${env.TEST_OUTPUT_FILENAME}' \
                             ${env.WORKSPACE}/RunDockerImage.sh
                    """
                    def numErrors = getNumberOfErrors(env.TEST_OUTPUT_FILENAME)
                    sh "exit ${numErrors}"
                }
            }
        }
    }
    post {
        success {
            echo 'Build successful'
            commonCleanupProcedures()
        }
        failure {
            echo 'Build failed!'
            commonCleanupProcedures()
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
        script: "sudo docker container ls -aq --filter name=${ctrName}",
        returnStdout: true
    ).trim()
    
    RTN_VLU = (CONTAINER_ID == "") ? null : CONTAINER_ID
    echo "getContainerID(${ctrName}) returns: ${RTN_VLU}"
    return RTN_VLU
}

def getContainerName(String imgName){
    CONTAINER_NAME = sh (
        script: "echo ${env.IMAGE_NAME} | sed -e 's/tstimg/ctrimg/g'",
        returnStdout: true,
        encoding: 'UTF-8'
    ).trim()
    
    RTN_VLU = (CONTAINER_NAME == "") ? null : CONTAINER_NAME
    echo "getContainerName(${imgName}) returns: ${RTN_VLU}"
    return RTN_VLU
}

def cleanupBuild(){
    CONTAINER_NAME = getContainerName(env.IMAGE_NAME)
    CONTAINER_ID = getContainerID(CONTAINER_NAME)
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

def doesOutputFileExist(){
    OUTFILE_EXISTS = sh (
        script: "if [ -f ${env.OUTFILE_PATH} ]; then  echo 'True'; else echo 'False'; fi",
        returnStdout: true
    ).trim()
    
    return (OUTFILE_EXISTS == "True") ? true : false
}

def getNumberOfErrors(String resultsFile){
    if(doesOutputFileExist()){
        NUM_ERRORS = sh (
            script: "cat ${resultsFile} \
                     | grep -o '[0-9]** error in [0-9]*\\.[0-9]* seconds =========' \
                     | cut -d' ' -f1",
            returnStdout: true
        ).trim()
        
        return NUM_ERRORS.toInteger()
    }
    else{
        return -1
    }
}

def commonCleanupProcedures(){
    if(doesOutputFileExist()){
        def numErrors = getNumberOfErrors(env.OUTFILE_PATH)
        if(numErrors > 0){
            sh "cat ${env.OUTFILE_PATH}"
        }
        echo "Automated testing completed with ${numErrors} errors"
        echo "Test results are in ${env.OUTFILE_PATH}"
    }
    cleanupBuild()
}
