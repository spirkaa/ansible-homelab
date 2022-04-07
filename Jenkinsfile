pipeline {
  agent any

  options {
    buildDiscarder(logRotator(numToKeepStr: '10', daysToKeepStr: '60'))
    parallelsAlwaysFailFast()
  }

  environment {
    REGISTRY = 'git.devmem.ru'
    REGISTRY_CREDS_ID = 'gitea-user'
    IMAGE_OWNER = 'cr'
    IMAGE_NAME = 'ansible'
    IMAGE_TAG = 'latest'
    DOCKERFILE = '.docker/Dockerfile'
    LABEL_AUTHORS = 'Ilya Pavlov <piv@devmem.ru>'
    LABEL_TITLE = 'Ansible'
    LABEL_DESCRIPTION = 'Ansible with collections'
    LABEL_URL = 'https://www.ansible.com'
    LABEL_CREATED = sh(script: "date '+%Y-%m-%dT%H:%M:%S%:z'", returnStdout: true).toString().trim()
  }

  stages {
    stage('Build image') {
      steps {
        script{
          docker.withRegistry("https://${REGISTRY}", "${REGISTRY_CREDS_ID}") {
            env.DOCKER_BUILDKIT = 1
            CACHE_FROM = "${REGISTRY}/${IMAGE_OWNER}/${IMAGE_NAME}:${IMAGE_TAG}"
            REVISION = GIT_COMMIT.take(7)

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
  }
}
