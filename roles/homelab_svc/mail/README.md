# Роль Ansible: Mail

Роль Ansible, которая запускает почтовый сервер в Docker контейнере:

* [tvial/docker-mailserver](https://hub.docker.com/r/tvial/docker-mailserver)
* [monogramm/autodiscover-email-settings](https://hub.docker.com/r/monogramm/autodiscover-email-settings)

## Зависимости

* Роль homelab_svc/traefik
* Роль homelab_svc/cadvisor
* Сертификат из роли `homelab_svc/traefik` в файле `../traefik/vars/cert.vault.yml`
* LDAP сервер из роли `homelab_svc/mgmt`
