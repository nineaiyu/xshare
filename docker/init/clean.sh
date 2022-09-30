#!/bin/bash
#
#

for i in nginx xshare mariadb redis buildclient build-buildxshare-1;do echo $i;docker rm -f $i;done


docker network rm xshare

