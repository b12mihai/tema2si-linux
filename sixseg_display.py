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

def interval_switch(dev_file, interval=DEFAULT_INTERVAL):

    f = open(dev_file, "w")    

    try:
        while(True):
            f.write(sixseg_display("only_hour"))
            #print sixseg_display("only_hour")
            time.sleep(interval) 
            f.write(sixseg_display("only_date"))
            #print sixseg_display("only_date")
            time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        f.close()
        sys.exit()

if __name__ == '__main__':

    f = open(CONF_DEV_FILE, "r")
    devfile = f.read().split('\n')[0]
    f.close()

    if(len(sys.argv) >= 3):
        interval_switch(str(sys.argv[1]), int(sys.argv[2]))
    else: 
        interval_switch(devfile, 2)  
