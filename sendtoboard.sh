#!/bin/bash

BOARD_IP=temasi.local

scp -r * root@$BOARD_IP:~/tema2 
ssh root@$BOARD_IP "/etc/init.d/si-server restart"
