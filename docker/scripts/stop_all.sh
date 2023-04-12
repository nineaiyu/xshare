#!/bin/bash
#
#


cd ../nginx/ && docker compose down

cd ../xshare/ && docker compose down

cd ../redis/ && docker compose down

cd ../mariadb/ && docker compose down
