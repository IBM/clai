pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile.CLAI'
    }

  }
  stages {
    stage('test') {
      steps {
        sh 'pytest'
      }
    }
  }
}