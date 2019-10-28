FROM ubuntu:18.04

RUN apt update; \
    apt install python-2.7 python-twisted python-mysqldb python-geoip python-watchdog docker; \
    git 
    pip install docker-py; \

ENTRYPOINT ./run.sh

