# Роль Ansible: Storage

Роль Ansible, которая устанавливает [mergerfs](https://github.com/trapexit/mergerfs) и [snapraid](https://www.snapraid.it/) и настраивает файловые системы.

## Сборка пакета snapraid для Debian 10 (Proxmox 6.4)

```shell
git clone https://github.com/IronicBadger/docker-snapraid
cd docker-snapraid
git checkout e210a4a
chmod +x build.sh
sudo ./build.sh 12.1
sudo chown -R 1000:1000 build
cp build/snapraid_12.1-1_amd64.deb ~/snapraid_12.1-1_amd64.deb
cd ..
rm -rf docker-snapraid
```

## Зависимости

Нет
