#!/usr/bin/env python

import time
import sys

CONF_DEV_FILE="/etc/epicclockpath"
DEFAULT_INTERVAL=5 #in seconds
DEFAULT_MODE="only_hour"

def sixseg_display(mode=DEFAULT_MODE):
    """
    Format the date/time to write to epic clock
    """
    if(mode == "only_hour"):
        output = time.strftime("%H%M%S") + '\n'
    elif(mode == "only_date"):
        output = time.strftime("%d%m%y") + '\n'
    else:
        print 'Invalid option'

    return output

def interval_switch(interval, dev_fd):

    while(True):
        dev_fd.write(sixseg_display("only_hour"))
        dev_fd.flush()
        time.sleep(interval)
        dev_fd.write(sixseg_display("only_date"))
        dev_fd.flush()
        time.sleep(interval)

if __name__ == '__main__':

    f = open(CONF_DEV_FILE, "r")
    dev_file = f.read().split('\n')[0]
    f.close()

    dev_fd = open(dev_file, "w")

    if(len(sys.argv) >= 2):
        interval_switch(int(sys.argv[1]), dev_fd)
    else:
        interval_switch(DEFAULT_INTERVAL, sys.stdout)
