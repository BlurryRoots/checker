FROM ubuntu:14.04

# Set variable to supress warings when installing packages
ENV DEBIAN_FRONTEND noninteractive

# Upgrade base system
RUN apt-get update
RUN apt-get install -y python2.7
RUN apt-get install -y python-flask
RUN apt-get install -y build-essential python-dev python-uwsgidecorators
RUN apt-get install -y python-software-properties software-properties-common
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get install -y nginx

# configure nginx

# link with wsgi

VOLUME /src
WORKDIR /src

ENTRYPOINT sh init.sh
