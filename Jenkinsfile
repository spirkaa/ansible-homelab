pipeline {
  agent any

  options {
    buildDiscarder(logRotator(numToKeepStr: '10', daysToKeepStr: '60'))
    parallelsAlwaysFailFast()
    disableConcurrentBuilds()
  }

  environment {
    REGISTRY = 'git.devmem.ru'
    REGISTRY_URL = "https://${REGISTRY}"
    REGISTRY_CREDS_ID = 'gitea-user'
    ANSIBLE_CREDS_ID = 'jenkins-ssh-key'
    ANSIBLE_VAULT_CREDS_ID = 'ansible-homelab-vault-password'
    ANSIBLE_IMAGE = "${REGISTRY}/cr/ansible:base"
  }

  parameters {
    string(name: 'ANSIBLE_PLAYBOOK', defaultValue: 'main.yml', description: 'Playbook name')
    string(name: 'ANSIBLE_EXTRAS', defaultValue: '--skip-tags create,dyn_inventory,portainer_api,cadvisor,jenkins', description: 'ansible-playbook extra params')
  }

  stages {
    stage('Run playbook') {
      agent {
        docker {
          image env.ANSIBLE_IMAGE
          registryUrl env.REGISTRY_URL
          registryCredentialsId env.REGISTRY_CREDS_ID
          alwaysPull true
          reuseNode true
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
    }
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
