FROM python:3.10-bullseye AS build

RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y libsasl2-dev libldap2-dev libssl-dev \
    && pip wheel --wheel-dir=/tmp python-ldap


FROM python:3.10-slim-bullseye AS prod

COPY --from=build /tmp/*.whl /tmp/

RUN apt-get update -y \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-suggests --no-install-recommends \
        git \
        libldap-2.4-2 \
        openssh-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.* /

RUN pip install --no-cache-dir -U pip wheel \
    && pip install /tmp/*.whl \
    && pip install --no-cache-dir -r /requirements.txt

RUN ansible-galaxy role install -r /requirements.yml -p /usr/share/ansible/roles \
    && ansible-galaxy collection install --no-cache -r /requirements.yml -p /usr/share/ansible/collections \
    && rm -rf /root/.ansible

CMD [ "/bin/bash" ]
