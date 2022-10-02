#!/bin/bash
#
#

cd ../build/
docker-compose build
docker-compose up buildclient
