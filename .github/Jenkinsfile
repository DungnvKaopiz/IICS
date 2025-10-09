pipeline {
  agent any
  environment {
    // credentials('github-token') là ID credential trên Jenkins (nếu cần)
    GITHUB_TOKEN = credentials('github-token')
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      when { expression { return env.CHANGE_ID == null ? false : true } } // chạy stage này chỉ cho PR
      steps {
        sh 'echo "Build for PR #${CHANGE_ID} from ${CHANGE_BRANCH} to ${CHANGE_TARGET}"'
        sh 'echo "Demo build: chạy unit tests..."'
        // put your actual build/test commands here
      }
    }
    stage('Non-PR tasks') {
      when { expression { return env.CHANGE_ID == null } } // chạy khi không phải PR (ví dụ main branch)
      steps { sh 'echo "Normal branch build"' }
    }
  }
  post {
    always {
      script {
        if (env.CHANGE_ID) {
          echo "PR build finished. PR=${env.CHANGE_ID}, from=${env.CHANGE_BRANCH}, to=${env.CHANGE_TARGET}"
        }
      }
    }
  }
}
