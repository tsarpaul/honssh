FROM ubuntu:18.04

RUN apt update; \
    apt install -y python python-pip python-twisted python-mysqldb python-geoip python-watchdog \
    git \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable" && \
    apt-get update && \
    apt-get install docker-ce-cli

RUN pip install docker-py
ADD ./ /honssh
RUN rm -f honssh.pid && cd /honssh && ./update.sh

WORKDIR /honssh
ENTRYPOINT ["./honsshctrl.sh", "start"]

