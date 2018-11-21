#!/bin/sh
echo "run dev: " ${ENV}

mv /etc/kong/kong.${ENV}.conf /etc/kong/kong.conf
/docker-entrypoint.sh $1 $2