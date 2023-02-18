# Ansible-Homelab

Репозиторий, в котором собрана конфигурация моих домашних серверов и развернутых на них приложений. И еще некоторые побочные плейбуки и роли, потому что лень создавать отдельный репозиторий и есть зависимости между ролями.

## Использование

* Одна команда для настройки хостов Proxmox, настройки DNS, создания контейнеров LXC и запуска в них сервисов на Docker

```shell
ansible-playbook main.yml
```

* Чтобы сократить время выполнения, можно запускать отдельные задачи с помощью тегов
  * `pve` - все задачи для хостов Proxmox
  * `pve_common` - отдельная задача для хостов Proxmox
  * `svc` - задачи сразу для всех docker-контейнеров
  * `mgmt` (имя хоста) - задачи для конкретного хоста LXC
  * `portainer` (имя контейнера) - задачи для конкретного docker-контейнера
  * `upgrade_packages` - обновление пакетов на всех хостах LXC
  * `dns` - задачи для DNS-сервера на роутере

```shell
ansible-playbook main.yml -t svc
```

## Ansible Vault

Строка

```shell
ansible-vault encrypt_string --encrypt-vault-id default --vault-password-file .vault_password --stdin-name 'secret'
```

Файл

```shell
ansible-vault decrypt group_vars/all/vault.yml --vault-password-file .vault_password
ansible-vault encrypt group_vars/all/vault.yml
```

## Как добавить новое приложение

1. Конфигурация в Ansible
2. Записи DNS в `deploy_homelab_set_static_dns.yml` для локального доступа через Traefik
3. Записи DNS на хостинге для доступа через интернет
4. Прокси хост в `Nginx Proxy Manager`
5. Пользователи в группе приложения в `FreeIPA`
