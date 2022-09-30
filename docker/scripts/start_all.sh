#!/bin/bash
#
#

cd ../mariadb/ && docker-compose up -d
cd ../redis/ && docker-compose up -d

cd ../xshare/ && docker-compose up -d
cd ../nginx/ && docker-compose up -d
docker logs -f xshare
