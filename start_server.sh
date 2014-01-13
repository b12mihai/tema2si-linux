#!/bin/bash

#Configure DNS
echo "nameserver 8.8.8.8" > /etc/resolv.conf

if [ $# -ge 1 ]; then
    echo "Starting web server on port: $1"
    PORT=$1
else
    echo "Starting web server on port 80"
    PORT=80
fi

#If we really want the webserver on PORT 80
#if [ $PORT -eq 80 ]; then
#	echo "This action is needed in order to start python"
#	/etc/init.d/lighttpd stop
#fi

mkdir /var/log/si_server/
python web_server.py $PORT &> /var/log/si_server/srv_stdout.log
