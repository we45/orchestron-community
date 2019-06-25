FROM ubuntu:16.04

RUN apt-get update --fix-missing && apt-get install -y wget apt-transport-https git-core vim curl build-essential python2.7-dev libssl-dev libffi-dev \
	libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev \
	python3-tk libxml2-dev libxslt1-dev supervisor  libfontconfig1 chrpath libxft-dev \
	libmysqlclient-dev python-software-properties software-properties-common libsasl2-dev python3-dev libldap2-dev \
	libfreetype6 libfontconfig1-dev netcat

COPY requirements.txt /webapps/orchestron_community_api/requirements.txt
COPY gunstart /webapps/orchestron_community_api/
COPY orchy_api.conf /etc/supervisor/conf.d/

RUN	chmod +x /webapps/orchestron_community_api/gunstart && mkdir /webapps/orchestron_community_api/logs

RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && pip3 install -r /webapps/orchestron_community_api/requirements.txt && pip3 install gunicorn pillow
COPY /orchy_project /webapps/orchestron_community_api

COPY migrations.sh /webapps/orchestron_community_api/
COPY wait-for /webapps/orchestron_community_api/
RUN chmod +x /webapps/orchestron_community_api/wait-for && chmod +x /webapps/orchestron_community_api/migrations.sh
WORKDIR /webapps/orchestron_community_api/

ENV C_FORCE_ROOT="True"

CMD supervisord
