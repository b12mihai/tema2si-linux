import web
import sys
import SimpleHTTPServer
import cgi
import os
import logging
import subprocess
import logging.handlers as handlers

import sixseg_display

urls = (
    '/',        'index',
    '/ControlNTP',  'ControlNTP',
    '/DevPath',     'DevPath',
    '/SetTimezone',     'SetTimezone',
    '/ConfigDisplay',   'ConfigDisplay'
)


#Used by subprocess, in order to be killed anytime
proc1 = None

#Configure interface logger.ing
class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        # If rotation/rollover is wanted, it doesn't make sense to use another
        # mode. If for example 'w' were specified, then if there were multiple
        # runs of the calling application, the logs from previous runs would be
        # lost if the 'w' is respected, because the log file would be truncated
        # on each run.
        if maxBytes > 0:
            mode = 'a'
        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes


log_filename='/var/log/si_server/actions.log'

directory = os.path.dirname(log_filename)

try:
    os.stat(directory)
except:
    os.mkdir(directory)

logger=logging.getLogger('Tema2SI_Linux_Logger')
logger.setLevel(logging.DEBUG)
handler=SizedTimedRotatingFileHandler(
        log_filename, maxBytes=100, backupCount=5,
        when='s',interval=10,
        # encoding='bz2',  # uncomment for bz2 compression
        )
logger.addHandler(handler)

render = web.template.render('templates/')

class index:
    def GET(self):
        #print 'Our PID is: ', os.getpid()
        logger.info("User went to homepage")
        logger.debug("Server's PID is %s" % str(os.getpid()))
        return render.index("Whoever looks at this homework")

    def POST(self):
        i = web.input()
        print 'TODO'

class ControlNTP:
    def GET(self):
        print 'TODO'

    def POST(self):
        i = web.input()
        logger.info("User wants to control NTP")
        cmd = i.controlNTP

        if cmd == 'start':
            proc = subprocess.Popen("/etc/init.d/ntpd start && cat /var/run/ntp.pid", stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            logger.info("Command /etc/init.d/ntpd start && cat /var/run/ntp.pid was issued to the system")
            return render.ntpsubmit(cmd="start",status=str(out)+str(err))
        elif cmd == 'stop':
            proc = subprocess.Popen("/etc/init.d/ntpd stop", stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            logger.info("Command /etc/init.d/ntpd stop was issued to the system")
            return render.ntpsubmit(cmd="stop",status=str(out)+str(err))
        else:
            logger.debug("Invalid NTP command entered by user")
            return render.ntpsubmit("dummy")

class DevPath:
    def GET(self):
        print 'TODO'

    def POST(self):
        i = web.input()
        f = open('/etc/epicclockpath', 'w')
        logger.info("User wants to write %s to /etc/epicclockpath" % (i.path))
        f.write(i.path + '\n')
        f.close()
        return render.epicclockpath(str(i.path))

class SetTimezone:
    def GET(self):
        print 'TODO'

    def POST(self):
        i = web.input()

        tzset_cmd = "cp /usr/share/zoneinfo/%s /etc/localtime" % (i.timezone)

        proc = subprocess.Popen(tzset_cmd, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        logger.info("Command %s was issued to system" % (tzset_cmd))
        proc = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        return render.tzone(str(i.timezone), str(out))

class ConfigDisplay:
    def GET(self):
        print 'TODO'

    def POST(self):
        global proc1
        i = web.input()
        f = open(sixseg_display.CONF_DEV_FILE, "r")
        dev_file = f.read().split('\n')[0]
        f.close()

        if(i.configdisp == '0' or i.configdisp == '1'):
            if(proc1 != None):
                proc1.kill()

        if(i.configdisp == '0'):
        #se va afisa doar ora
            f = open(dev_file, "w")
            f.write(sixseg_display.sixseg_display("only_hour"))
            f.close()
            logger.info("User wanted to print only_hour" % (cmd))

        elif(i.configdisp == '1'):
        #se va afisa doar data
            f = open(dev_file, "w")
            f.write(sixseg_display.sixseg_display("only_date"))
            f.close()
        elif(i.configdisp == '2'):
        #povestea cu intervalul etc.
            cmd = "/home/root/tema2/sixseg_display.py %s %s" % (str(i.configdisp), str(i.dispinterval))
            proc1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        else:
            #We should not be here
            assert(0)

        return render.disp(str(i.configdisp), str(i.dispinterval))

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    print sixseg_display.sixseg_display.__doc__
    app.run()
