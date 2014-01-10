#!/bin/bash

#python web_server.py &> server.log

if [ $# -ge 1 ]; then
    echo "Starting web server on port: $1"
    PORT=$1
else
    echo "Starting web server on port 1991"
    PORT=1991
fi

mkdir /var/log/si_server
python web_server.py $PORT
