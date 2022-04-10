.POSIX:

TAG=git.devmem.ru/cr/ansible

default: run

build:
	@DOCKER_BUILDKIT=1 docker build --tag ${TAG} -f .docker/Dockerfile .

run:
	@docker run \
		--pull always \
		--rm \
		--interactive \
		--tty \
		--network host \
		--env "TZ=Europe/Moscow" \
		--env "TERM=${TERM}" \
		--env "HOME=${HOME}" \
		--volume "${HOME}:${HOME}" \
		--volume "/etc/passwd:/etc/passwd" \
		--user "$(shell id -u ${USER}):$(shell id -g ${USER})" \
		--workdir "$(shell pwd)" \
		${TAG}
