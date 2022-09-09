pipeline {
  agent {
    docker {
      image 'git.devmem.ru/projects/ansible:base'
      registryUrl 'https://git.devmem.ru'
      registryCredentialsId 'gitea-user'
      alwaysPull true
      reuseNode true
      args '-v /tmp/.cache:/tmp/.cache'
    }
  }

  options {
    buildDiscarder(logRotator(numToKeepStr: '10', daysToKeepStr: '60'))
    parallelsAlwaysFailFast()
    disableConcurrentBuilds()
  }

  triggers {
    cron(BRANCH_NAME == 'main' ? 'H 10 * * 6' : '')
  }

  environment {
    ANSIBLE_CREDS_ID = 'jenkins-ssh-key'
    ANSIBLE_VAULT_CREDS_ID = 'ansible-homelab-vault-password'
  }

  parameters {
    string(name: 'ANSIBLE_PLAYBOOK', defaultValue: 'main.yml', description: 'Playbook name')
    string(name: 'ANSIBLE_EXTRAS', defaultValue: '--skip-tags create,dyn_inventory,portainer_api,reboot,cadvisor,jenkins', description: 'ansible-playbook extra params')
  }

  stages {
    stage('Run pre-commit') {
      steps {
        cache(path: "/tmp/.cache/pre-commit", key: "pre-commit-${hashFiles('**/.pre-commit-config.yaml')}") {
          sh '''#!/bin/bash
            PRE_COMMIT_HOME=/tmp/.cache/pre-commit pre-commit run --all-files --verbose --color always
          '''
        }
      }
    }

    stage('Run playbook') {
      when {
        branch 'main'
        anyOf {
          triggeredBy cause: 'UserIdCause'
          triggeredBy 'TimerTrigger'
        }
      }
      steps {
        sh 'ansible --version'
        withCredentials([string(credentialsId: "${ANSIBLE_VAULT_CREDS_ID}", variable: 'ANSIBLE_VAULT_PASS')]) {
          sh 'echo $ANSIBLE_VAULT_PASS > .vault_password'
        }
        ansiblePlaybook(
          colorized: true,
          credentialsId: "${ANSIBLE_CREDS_ID}",
          playbook: "${params.ANSIBLE_PLAYBOOK}",
          extras: "${params.ANSIBLE_EXTRAS}"
        )
      }
      post {
        always {
          emailext(
            to: '$DEFAULT_RECIPIENTS',
            subject: '$DEFAULT_SUBJECT',
            body: '$DEFAULT_CONTENT'
          )
        }
      }
    }
  }
}
