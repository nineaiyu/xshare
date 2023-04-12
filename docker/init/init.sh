#!/bin/bash
#
#

which dockerd
if [ $? -ne 0 ];then
	dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
	dnf install docker-ce -y
fi

data_path="$(dirname $(dirname `pwd`))/data"
mkdir -pv ${data_path}/{web,mariadb,redis,logs/{mariadb,nginx,xshare}}
chown 1001.1001 -R ${data_path}/{web,mariadb,redis,logs/{mariadb,nginx,xshare}}
systemctl start docker && docker network create xshare --driver bridge --subnet=172.31.32.0/24
systemctl enable docker
systemctl status docker


#docker pull 'bitnami/mariadb:10.7.3'
#docker pull 'bitnami/redis:6.2.7'
#docker pull 'nginx:1.21.3'
#docker pull 'node:14.17.3'
