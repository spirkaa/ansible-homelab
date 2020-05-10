# Ansible-Homelab

Репозиторий, в котором собрана конфигурация моих домашних серверов и развернутых на них приложений.

## Команды для кластера Kubernetes

* Одна команда, чтобы сделать всё

      ansible-playbook main.yml -i hosts --vault-password-file ~/.passwd

* Если кластер уже есть, можно пропустить все шаги настройки и сразу сгенерировать Inventory, установить тестовое приложение в кластере

      ansible-playbook main.yml -i hosts --vault-password-file ~/.passwd -t dyn_inventory,deploy_hello_k8s

* Завершить работу ВМ

      ansible-playbook main.yml -i hosts --vault-password-file ~/.passwd -t shutdown

* Запустить ВМ

      ansible-playbook main.yml -i hosts --vault-password-file ~/.passwd -t start

* Удалить ВМ и начать всё сначала первой командой в списке

      ansible-playbook main.yml -i hosts --vault-password-file ~/.passwd -t destroy
