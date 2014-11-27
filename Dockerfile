FROM ubuntu:14.04

# Set variable to supress warings when installing packages
ENV DEBIAN_FRONTEND noninteractive

# Upgrade base system
RUN apt-get update
RUN apt-get install -y python2.7
RUN apt-get install -y python-flask

VOLUME /src
WORKDIR /src

ENTRYPOINT sh init.sh
