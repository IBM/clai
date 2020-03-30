// Licensed Materials - Property of IBM
//
// ????-??? Copyright IBM Corp. 2020 All Rights Reserved.
//
// US Government Users Restricted Rights - Use, duplication or
// disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

pipeline {
    agent { dockerfile true }
    
    stages {
        stage('begin') {
            steps {
                script{
                    sh "${env.WORKSPACE}/checkJenkinsPreconditions.sh"
                }
            }
        }
        
        stage ('test') {
            steps {
                sh """
                    pytest
                """
            }
        }
    }
    post {
        success {
            echo 'Do something when it is successful'
        }
        failure {
            echo 'Do something when it is failed'
        }
    }
}