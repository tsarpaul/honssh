FROM ubuntu:18.04

RUN apt update; \
    apt install -y python python-pip python-twisted python-mysqldb python-geoip python-watchdog docker git
RUN pip install docker-py
RUN git clone https://github.com/tsarpaul/honssh /honssh && \
    /honssh/update.sh

WORKDIR /honssh
ENTRYPOINT ["/honssh/honsshctrl.sh", "start"]

