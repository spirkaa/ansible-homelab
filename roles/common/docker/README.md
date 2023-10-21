# Роль Ansible: Docker

Роль Ansible, которая устанавливает и настраивает Docker и docker-compose так, чтобы докером можно было управлять через TCP, а модуль Ansible с говорящим названием `docker_compose` при попытке его использования не выдавал ошибок и нормально работал (<https://github.com/ansible-collections/community.docker/issues/216>).

## Зависимости

- geerlingguy.pip
- geerlingguy.docker
