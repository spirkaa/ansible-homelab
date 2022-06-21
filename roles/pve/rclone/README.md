# Роль Ansible: rclone

Роль Ansible, которая устанавливает и настраивает [rclone](https://github.com/rclone/rclone).

## Зависимости

Нет

## Как добавить новое задание

1. На сервере с помощью `rclone config` создать remote
1. На сервере скопировать параметры remote из `.config/rclone/rclone.conf` в `rclone_configs.vault.yml`
1. Настроить расписание в переменной `rclone_sync_config`
