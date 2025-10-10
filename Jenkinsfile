pipeline {
  agent any
  environment {
    GITHUB_TOKEN = credentials('iics-git-pat')
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
        script {
          // Load TASK_ID/TASK_TYPE from an env file in the repo (format: KEY=VALUE per line)
          def envFilePath = 'test_scripts/iics.env'
          def envPairs = []
          if (fileExists(envFilePath)) {
            def content = readFile(envFilePath).trim()
            envPairs = content.split('\n').collect { line ->
              line = line.trim()
              if (!line || line.startsWith('#')) { return null }
              def parts = line.split('=', 2).collect { it.trim() }
              return parts.size() == 2 ? "${parts[0]}=${parts[1]}" : null
            }.findAll { it != null }
          } else {
            error("Environment file not found: ${envFilePath}")
          }

          withCredentials([
            usernamePassword(credentialsId: 'iics-creds', usernameVariable: 'IICS_USER', passwordVariable: 'IICS_PASS')
          ]) {
            // Expose TASK_ID / TASK_TYPE from the env file to the shell and Jenkins env
            withEnv(envPairs) {
              // Run trigger script and capture outputs
              def out = sh(script: '''
  export IICS_USER="${IICS_USER}"
  export IICS_PASS="${IICS_PASS}"
  python3 test_scripts/trigger_iics_job.py
''', returnStdout: true).trim()
              echo out
              def runIdMatcher = (out =~ /::set-output name=runId::(.*)/)
              def serverUrlMatcher = (out =~ /::set-output name=serverUrl::(.*)/)
              def sessionIdMatcher = (out =~ /::set-output name=sessionId::(.*)/)
              if (!runIdMatcher) {
                error('Failed to obtain runId from trigger script output')
              }
              env.RUN_ID = runIdMatcher[0][1].trim()
              env.SERVER_URL = serverUrlMatcher ? serverUrlMatcher[0][1].trim() : ''
              env.SESSION_ID = sessionIdMatcher ? sessionIdMatcher[0][1].trim() : ''
              // Make sure Jenkins env contains TASK_ID / TASK_TYPE for downstream steps
              env.TASK_ID = env.TASK_ID ?: "${TASK_ID}"
              env.TASK_TYPE = env.TASK_TYPE ?: "${TASK_TYPE}"
            }
          }

          // Monitor the job (monitor script uses env.RUN_ID, env.SERVER_URL, env.SESSION_ID, env.TASK_ID)
          try {
            sh 'python3 test_scripts/monitor_iics_job.py'
            echo "IICS job completed successfully. Build done."
          } catch (err) {
            error("IICS job failed or timed out: ${err}")
          }
        }
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
