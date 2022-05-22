.POSIX:

TAG=git.devmem.ru/projects/ansible:base

default: tools

tools:
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

run:
	@ansible-playbook main.yml \
		--skip-tags create,dyn_inventory,portainer_api,cadvisor
