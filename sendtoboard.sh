#!/bin/bash

BOARD_IP=temasi.local

scp -r * root@$BOARD_IP:~/tema2 #&& ssh root@$BOARD_IP "/home/root/tema2/start_server.sh"
