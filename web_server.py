import web
import SimpleHTTPServer
import cgi

import sys
import os
from textwrap import dedent

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

#Device driver
dev_fd = None

#Configure logging
import logging
import logging.handlers
import subprocess

#This is a default filename. If directory does not
#exist we will create it
log_filename='/var/log/si_server/actions.log'
directory = os.path.dirname(log_filename)
try:
    os.stat(directory)
except:
    os.mkdir(directory)

logger=logging.getLogger('Tema2SI_WebServer_Logger')

#This if is because Python is, honestly, stupid!
if not len(logger.handlers):
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("[%(asctime)s] %(name)s : %(levelname)s : %(message)s")

    # Add the log message handler to the logger
    # Using python`s logrotation
    handler = logging.handlers.RotatingFileHandler(log_filename, mode='a',
                                                    maxBytes=1000000,
                                                    backupCount=5)
    handler.setFormatter(fmt)
    logger.addHandler(handler)

#Let's also configure logging of the stdout:

# HTML web.py rendering
render = web.template.render('templates/')

class index:
    def GET(self):
        logger.debug("User with IP=%s went to homepage" % str(web.ctx['ip']))
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

        cmd = i.controlNTP
        logger.info("User-ul cu IP-ul %s a trimis comanda %s daemonului NTP"
        % (str(web.ctx['ip']), str(i.controlNTP)))

        if cmd == 'start':
            proc = subprocess.Popen("/etc/init.d/ntpd start && cat /var/run/ntp.pid", stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            logger.debug("Command /etc/init.d/ntpd start && cat /var/run/ntp.pid was issued to the system")
            return render.ntpsubmit(cmd="start",status=str(out)+str(err))
        elif cmd == 'stop':
            proc = subprocess.Popen("/etc/init.d/ntpd stop", stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            logger.debug("Command /etc/init.d/ntpd stop was issued to the system")
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
        logger.info("User-ul cu IP-ul %s a scris %s in /etc/epicclockpath"
        % (str(web.ctx['ip']), str(i.path)))
        f.write(i.path + '\n')
        f.close()
        return render.epicclockpath(str(i.path))

class SetTimezone:
    def GET(self):
        print 'TODO'

    def POST(self):
        i = web.input()
        proc = subprocess.Popen("date +%Z", stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        crt_tz = out

        tzset_cmd = "cp /usr/share/zoneinfo/%s /etc/localtime" % (i.timezone)
        logger.debug("Command %s was issued to system" % tzset_cmd)

        proc = subprocess.Popen(tzset_cmd, stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        proc = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()

        logger.info("Userul cu IP-ul %s a schimbat timezone-ul din %s in %s"
        % ( str(web.ctx['ip']) , str(crt_tz), str(i.timezone) ) )
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

        dev_fd = open(dev_file, "w")

        if(i.configdisp == '0'):
        #se va afisa doar ora
            dev_fd.write(sixseg_display.sixseg_display("only_hour"))
            dev_fd.close()
            logger.info("User-ul cu IP-ul %s a modificat tipul de afisare: doar timpul"
            % (str(web.ctx['ip'])))

        elif(i.configdisp == '1'):
        #se va afisa doar data
            dev_fd.write(sixseg_display.sixseg_display("only_date"))
            dev_fd.close()
            logger.info("User-ul cu IP-ul %s a modificat tipul de afisare: doar data" % (str(web.ctx['ip'])))

        elif(i.configdisp == '2'):
        #povestea cu intervalul etc.
            cmd = "/home/root/tema2/sixseg_display.py %s" % (str(i.dispinterval))
            proc1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            logger.info("User-ul cu IP-ul %s a modificat tipul de afisare: se cicleaza intre afisarea datei si a orei cu intervalul %s"
            % (str(web.ctx['ip']), str(i.dispinterval) ) )

        else:
            #We should not be here
            assert(0)

        return render.disp(str(i.configdisp), str(i.dispinterval))

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    print sixseg_display.sixseg_display.__doc__
    app.run()
