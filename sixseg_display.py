#!/usr/bin/env python

import time
import sys

CONF_DEV_FILE="/etc/epicclockpath"
DEFAULT_INTERVAL=1 #in seconds
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
    
def write_realtime(interval, dev_fd):
    
    while(True):
        dev_fd.write(sixseg_display("only_hour"))
        time.sleep(interval)
        dev_fd.flush()

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
    
    if(len(sys.argv) < 2):
        sys.stderr.write("USAGE: sixseg_display mode [interval]. mode can be {time | date | time_date_sw}")
        sys.exit(-1)
    
    dev_fd = open(dev_file, "w")
    
    mode = str(sys.argv[1])
    try:
        interval = int(sys.argv[2])
    except:
        interval = DEFAULT_INTERVAL
    
    if(mode == "time"):
        write_realtime(interval, dev_fd)
    elif(mode == "date"):
        dev_fd.write(sixseg_display("only_date"))
    elif(mode == "time_date_sw"):
        interval_switch(interval, dev_fd)
    else:
        assert 0, "Invalid option provided by user"

