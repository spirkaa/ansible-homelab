# Роль Ansible: Storage

Роль Ansible, которая устанавливает [mergerfs](https://github.com/trapexit/mergerfs) и [snapraid](https://www.snapraid.it/) и настраивает файловые системы.

## Сборка пакета snapraid для Debian 11 (Proxmox 7.2)

```shell
git clone https://github.com/IronicBadger/docker-snapraid
cd docker-snapraid
sudo ./build.sh 12.2
sudo chown -R 1000:1000 build
cp build/snapraid-from-source.deb ~/snapraid_12.2-1_amd64.deb
cd ..
rm -rf docker-snapraid
```

## Зависимости

Нет
