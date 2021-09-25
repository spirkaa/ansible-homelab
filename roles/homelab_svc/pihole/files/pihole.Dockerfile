FROM pihole/pihole:latest
LABEL maintainer="Ilya Pavlov <piv@devmem.ru>"

ARG REMOTE_URL=https://raw.githubusercontent.com/jacklul/pihole-updatelists/master

RUN set -eux \
    && curl -o /usr/local/sbin/pihole-updatelists "${REMOTE_URL}/pihole-updatelists.php" \
    && chmod +x /usr/local/sbin/pihole-updatelists \
    && curl -o /etc/pihole-updatelists.conf "${REMOTE_URL}/pihole-updatelists.conf"

RUN set -eux \
    && echo "0 4 * * 7 root /usr/local/sbin/pihole-updatelists > /dev/null 2>&1" >> /etc/cron.d/pihole
