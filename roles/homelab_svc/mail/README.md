# Роль Ansible: Mail

Роль Ansible, которая запускает почтовый сервер в Docker контейнере:

* [mailserver/docker-mailserver](https://hub.docker.com/r/mailserver/docker-mailserver/tags)
* [monogramm/autodiscover-email-settings](https://hub.docker.com/r/monogramm/autodiscover-email-settings/tags)

## Зависимости

* Роль homelab_svc/traefik
* Роль homelab_svc/cadvisor
* LDAP сервер из роли `homelab_svc/mgmt`
