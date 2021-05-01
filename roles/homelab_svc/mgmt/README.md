# Роль Ansible: Management

Роль Ansible, которая запускает Docker контейнеры:

* [vaultwarden/server](https://hub.docker.com/r/vaultwarden/server/tags)
* [freeipa/freeipa-server](https://hub.docker.com/r/freeipa/freeipa-server/tags) + [osixia/phpldapadmin](https://hub.docker.com/r/osixia/phpldapadmin/tags)
* [linuxserver/heimdall](https://hub.docker.com/r/linuxserver/heimdall/tags)
* [portainer/portainer-ce](https://hub.docker.com/r/portainer/portainer-ce/tags)
* [linuxserver/unifi-controller](https://hub.docker.com/r/linuxserver/unifi-controller/tags)
* [nico640/docker-unms](https://hub.docker.com/r/nico640/docker-unms/tags)

## Зависимости

* Роль homelab_svc/traefik
* Роль homelab_svc/cadvisor

## Заметки

### Служебная учетная запись для доступа к FreeIPA

То же самое, только в стиле DevGitSecOps, можно сделать и с помощью модуля [ldap_entry](https://docs.ansible.com/ansible/latest/modules/ldap_entry_module.html) в Ansible.

<https://www.freeipa.org/page/HowTo/LDAP#System_Accounts>

Если в какой-нибудь системе можно авторизоваться через LDAP, при этом не требуется редактирование данных LDAP с помощью этой системы, то для доступа к каталогу нужно создать служебную учетную запись, которая работает только для чтения.

На хосте mgmt выполнить команду `docker exec -it freeipa sh -c 'ldapmodify -x -D "cn=Directory Manager" -W'` и ввести пароль от Directory Manager. Затем вставить блок текста, предварительно заменив в нём значения `uid` и `userPassword`. Каждое значение с новой строки. Пустая строка в конце.

    dn: uid=demosvc,cn=sysaccounts,cn=etc,dc=home,dc=devmem,dc=ru
    changetype: add
    objectclass: account
    objectclass: simplesecurityobject
    uid: demosvc
    userPassword: passwrd246
    passwordExpirationTime: 20380119031407Z
    nsIdleTimeout: 0
