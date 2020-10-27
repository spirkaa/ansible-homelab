# Роль Ansible: Development

Роль Ansible, которая запускает Docker контейнеры:

* [linuxserver/code-server](https://hub.docker.com/r/linuxserver/code-server/tags)
* [gitea/gitea](https://hub.docker.com/r/gitea/gitea/tags) + [yobasystems/alpine-mariadb](https://hub.docker.com/r/yobasystems/alpine-mariadb/tags)
* [drone/drone](https://hub.docker.com/r/drone/drone/tags) + [drone/drone-runner-docker](https://hub.docker.com/r/drone/drone-runner-docker/tags)
* [registry](https://hub.docker.com/_/registry?tab=tags) + [joxit/docker-registry-ui](https://hub.docker.com/r/joxit/docker-registry-ui/tags)

## Зависимости

* Роль homelab_svc/traefik
* Роль homelab_svc/cadvisor

## Заметки

### Включить метрики Drone

<https://docs.drone.io/server/metrics/>

1. Сгенерировать токен

        $ openssl rand -hex 16
          fe8c402a51e6629aa1f43a4234afee81

1. Создать пользователя

        $ docker run --rm -it --entrypoint="" drone/cli:latest \
          drone -s $DRONE_SERVER -t $DRONE_TOKEN \
          user add prometheus --admin --machine \
          --token=fe8c402a51e6629aa1f43a4234afee81

          Successfully added user fe8c402a51e6629aa1f43a4234afee81
          Generated account token kRKuQ2JM0ahkEo2rjXnz3RCrBG1IfF7h

1. Настроить Prometheus

        - job_name: 'drone'
            scheme: https
            bearer_token: kRKuQ2JM0ahkEo2rjXnz3RCrBG1IfF7h
            static_configs:
            - targets: ['drone.domain.com']

### Включить метрики Gitea

<https://docs.gitea.io/en-us/config-cheat-sheet/#metrics-metrics>

1. Сгенерировать токен

        $ openssl rand -hex 16
          fa021205d4ce2cce14b692b60ea6df1b

1. Настроить Gitea

        $ nano gitea/conf/app.ini
          [metrics]
          ENABLED=true
          TOKEN=fa021205d4ce2cce14b692b60ea6df1b

1. Настроить Prometheus

        - job_name: 'gitea'
            scheme: https
            bearer_token: fa021205d4ce2cce14b692b60ea6df1b
            static_configs:
            - targets: ['gitea.domain.com']
