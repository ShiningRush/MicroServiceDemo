#!/bin/sh
echo "run dev: " ${ENV}

mv /dnsmasq.${ENV}.conf /etc/dnsmasq.d/dnsmasq.conf

dnsmasq -k