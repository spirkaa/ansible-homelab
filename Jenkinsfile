pipeline {
  agent any

  options {
    buildDiscarder(logRotator(numToKeepStr: '10', daysToKeepStr: '60'))
    parallelsAlwaysFailFast()
    disableConcurrentBuilds()
  }

    triggers {
      cron('0 8 * * 5')
    }

  environment {
    REGISTRY = 'git.devmem.ru'
    REGISTRY_URL = "https://${REGISTRY}"
    REGISTRY_CREDS_ID = 'gitea-user'
    IMAGE_OWNER = 'cr'
    IMAGE_NAME = 'ansible'
    IMAGE_TAG = 'latest'
    DOCKERFILE = '.docker/Dockerfile'
    LABEL_AUTHORS = 'Ilya Pavlov <piv@devmem.ru>'
    LABEL_TITLE = 'Ansible'
    LABEL_DESCRIPTION = 'Ansible for CI/CD pipelines'
    LABEL_URL = 'https://www.ansible.com'
    LABEL_CREATED = sh(script: "date '+%Y-%m-%dT%H:%M:%S%:z'", returnStdout: true).toString().trim()
    CACHE_FROM = "${REGISTRY}/${IMAGE_OWNER}/${IMAGE_NAME}:${IMAGE_TAG}"
    REVISION = GIT_COMMIT.take(7)

    ANSIBLE_IMAGE = "${REGISTRY}/${IMAGE_OWNER}/${IMAGE_NAME}:${IMAGE_TAG}"
    ANSIBLE_PLAYBOOK = 'main.yml'
    ANSIBLE_CREDS_ID = 'jenkins-ssh-key'
    ANSIBLE_VAULT_CREDS_ID = 'ansible-homelab-vault-password'
  }

  stages {
    stage('Set env vars') {
      steps {
        script {
          env.DOCKER_BUILDKIT = 1
        }
      }
    }

    stage('Build image') {
      when {
        anyOf {
          changeset 'Jenkinsfile'
          changeset '.docker/Dockerfile'
          changeset 'requirements.*'
        }
      }
      steps {
        script {
          docker.withRegistry("${REGISTRY_URL}", "${REGISTRY_CREDS_ID}") {
            def myImage = docker.build(
              "${IMAGE_OWNER}/${IMAGE_NAME}:${IMAGE_TAG}",
              "--label \"org.opencontainers.image.created=${LABEL_CREATED}\" \
              --label \"org.opencontainers.image.authors=${LABEL_AUTHORS}\" \
              --label \"org.opencontainers.image.url=${LABEL_URL}\" \
              --label \"org.opencontainers.image.source=${GIT_URL}\" \
              --label \"org.opencontainers.image.version=${IMAGE_TAG}\" \
              --label \"org.opencontainers.image.revision=${REVISION}\" \
              --label \"org.opencontainers.image.title=${LABEL_TITLE}\" \
              --label \"org.opencontainers.image.description=${LABEL_DESCRIPTION}\" \
              --progress=plain \
              --cache-from ${CACHE_FROM} \
              -f ${DOCKERFILE} ."
            )
            myImage.push()
            // Untag and remove image by sha256 id
            sh "docker rmi -f \$(docker inspect -f '{{ .Id }}' ${myImage.id})"
          }
        }
      }
    }

    stage('Build image (no cache)') {
      when {
        anyOf {
          triggeredBy 'TimerTrigger'
          triggeredBy cause: 'UserIdCause'
        }
      }
      steps {
        script {
          docker.withRegistry("${REGISTRY_URL}", "${REGISTRY_CREDS_ID}") {
            def myImage = docker.build(
              "${IMAGE_OWNER}/${IMAGE_NAME}:${IMAGE_TAG}",
              "--label \"org.opencontainers.image.created=${LABEL_CREATED}\" \
              --label \"org.opencontainers.image.authors=${LABEL_AUTHORS}\" \
              --label \"org.opencontainers.image.url=${LABEL_URL}\" \
              --label \"org.opencontainers.image.source=${GIT_URL}\" \
              --label \"org.opencontainers.image.version=${IMAGE_TAG}\" \
              --label \"org.opencontainers.image.revision=${REVISION}\" \
              --label \"org.opencontainers.image.title=${LABEL_TITLE}\" \
              --label \"org.opencontainers.image.description=${LABEL_DESCRIPTION}\" \
              --progress=plain \
              --pull \
              --no-cache \
              -f ${DOCKERFILE} ."
            )
            myImage.push()
            // Untag and remove image by sha256 id
            sh "docker rmi -f \$(docker inspect -f '{{ .Id }}' ${myImage.id})"
          }
        }
      }
    }

    stage('Run playbook') {
      when {
        not {
          triggeredBy 'TimerTrigger'
        }
      }
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
          playbook: "${ANSIBLE_PLAYBOOK}",
          credentialsId: "${ANSIBLE_CREDS_ID}"
        )
      }
    }
  }
}
