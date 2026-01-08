#!/usr/bin/env bash

# This is the sys_prep script
# It will clear out all non-revelent information for a new VM

sudo /sbin/service rsyslog stop
sudo /sbin/service auditd stop
#package-cleanup --oldkernels --count=1
sudo yum -y clean all
sudo rm -rf /var/cache/yum

# 1. Force logs to rotate and clear old.
sudo /usr/sbin/logrotate -f /etc/logrotate.conf
sudo /bin/rm -f /var/log/*-???????? /var/log/*.gz
sudo /bin/rm -f /var/log/dmesg.old

# 2. Clear the audit log & wtmp.
sudo /bin/cat /dev/null > /var/log/audit/audit.log
sudo /bin/cat /dev/null > /var/log/wtmp
sudo /bin/cat /dev/null > /var/log/lastlog
sudo /bin/cat /dev/null > /var/log/grubby

# 3. Remove the udev device rules.
sudo /bin/rm -f /etc/udev/rules.d/70*

# 4. Remove the traces of the template MAC address and UUIDs.
sudo /bin/sed -i '/^\(HWADDR\|UUID\|IPADDR\|NETMASK\|GATEWAY\)=/d' /etc/sysconfig/network-scripts/ifcfg-e*

# 5. Clean /tmp out.
sudo /bin/rm -rf /tmp/*
sudo /bin/rm -rf /var/tmp/*

# 6. Remove the SSH host keys.
sudo /bin/rm -f /etc/ssh/*key*

# 7. Remove the user's shell history.
sudo /bin/rm -f /home/centos/.bash_history
unset HISTFILE

# 8. Set hostname to localhost
sudo /bin/sed -i "s/HOSTNAME=.*/HOSTNAME=localhost.localdomain/g" /etc/sysconfig/network
sudo /bin/hostnamectl set-hostname localhost.localdomain

# 9. Remove rsyslog.conf remote log server IP.
sudo /bin/sed -i '/1.1.1.1.1/'d /etc/rsyslog.conf

# 10. clean hosts
hostname_check=$(hostname)
if ! [[ "${hostname_check}" =~ "local" ]]; then
    sudo cp -v /etc/hosts /etc/hosts.sys_prep
    sudo sed -i "s,$(hostname),,g" /etc/hosts
    sudo sed -i "s,$(hostname -s),,g" /etc/hosts
fi

sudo cloud-init clean

# 11. trim file system.
sudo fstrim /

# 12. Shutdown the VM. Poweron required to scan new HW addresses.
sudo poweroff
