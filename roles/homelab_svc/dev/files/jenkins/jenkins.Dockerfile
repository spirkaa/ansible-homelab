FROM jenkins/jenkins:alpine-jdk11

ENV JAVA_OPTS -Duser.timezone=Europe/Moscow -Djenkins.install.runSetupWizard=false

COPY --chown=jenkins:jenkins plugins.txt /usr/share/jenkins/ref/plugins.txt

RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt
