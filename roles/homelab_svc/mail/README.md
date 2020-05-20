# Роль Ansible: Mail

Роль Ansible, которая запускает почтовый сервер в Docker контейнере:

* [tvial/docker-mailserver](https://hub.docker.com/r/tvial/docker-mailserver)

## Зависимости

* Сертификат из роли `homelab_svc/traefik` в файле `../traefik/vars/cert.vault.yml`
* LDAP сервер из роли `homelab_svc/mgmt`
