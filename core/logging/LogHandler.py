import time
import pylabs
from pylabs.Shell import *
from logtargets.LogTargetFS import LogTargetFS
from pylabs.logging.LogConsoleController import LogConsoleController

try:
    from pylabs.logging.logtargets.LogTargetScribe import LogTargetScribe
except ImportError:
    pass

from pylabs.logging.logtargets.LogTargetToPylabsLogConsole import LogTargetToPylabsLogConsole
from pylabs.messages import toolStripNonAsciFromText
from pylabs.messages.LogObject import LogObject
from pylabs.decorators import deprecated

class LogHandler(object):

    def __init__(self):
        '''
        This empties the log targets
        '''
        self.maxlevel=6
        self.consoleloglevel=2
        self.lastmessage=""
        #self.lastloglevel=0
        self.logs=[]
        self.nolog=False
        self._fallbackLogger=LogTargetFS()
        self._lastcleanuptime=0
        self._lastinittime=9999999999  #every 5 seconds want to reinit the logger to make sure all targets which are available are connected
        self.logTargets = []
        self.console = LogConsoleController()
        self.inlog=False

    def _init(self):
        """
        called by pylabs
        """
        self._lastinittime=0
        self.nolog=True
        inifile=pylabs.q.config.getInifile("main")
        if inifile.checkParam("main","lastlogcleanup")==False:
            inifile.setParam("main","lastlogcleanup",0)
        self._lastcleanuptime=int(inifile.getValue("main","lastlogcleanup"))
        self.nolog=False
        self.logTargetAdd(LogTargetToPylabsLogConsole())
        try:
            self.logTargetAdd(LogTargetScribe())
        except:
            pylabs.q.logger.log("Could not add logtarget scribe")


    def _inittargets(self):
        """
        only execute this every hour
        """
        if self._lastinittime < pylabs.q.base.time.getTimeEpoch() - 3600:

            #check which loggers are not working
            for target in self.logTargets:
                if target.enabled==False:
                    try:
                        target.open()
                    except:
                        target.enabled = False
            self.cleanupLogsOnFilesystem()
            self._lastinittime=pylabs.q.base.time.getTimeEpoch()


    def log(self, message, level=5, tags="",dontprint=False):
        """
        send to all log targets
        """
        message=toolStripNonAsciFromText(message)
        if level<7:
            if self._fallbackLogger.enabled:
                self._fallbackLogger.log(message,level,tags)
        self._inittargets()
        if level<self.consoleloglevel+1 and dontprint==False:
            pylabs.q.console.echo(message,log=False)
        if self.nolog:
            return
        #if message<>"" and message[-1]<>"\n":
        #    message+="\n"
        if level<self.maxlevel+1:

            #print pylabs.q.application.state
            #if pylabs.q.application.state==pylabs.q.enumerators.AppStatusType.RUNNING:
            logobject=LogObject()
            logobject.init(message,level,tags)

            #add to active transaction when there is one
            if pylabs.q.transaction.activeTransaction<>None:
                if len (pylabs.q.transaction.activeTransaction.logs)>250:
                    pylabs.q.transaction.activeTransaction.logs=pylabs.q.transaction.activeTransaction.logs[-200:]
                pylabs.q.transaction.activeTransaction.logs.append(logobject)

            self.logs.append(logobject)
            if len (self.logs)>550:
                    self.logs=self.logs[-500:]

            #log to old logtargets
            source= pylabs.q.application.agentid+"_"+pylabs.q.application.appname
            messageold=self._encodeLog(message, level, logtype=1, source=source, tags=tags)
            for logtarget in self.logTargets:
                if (hasattr(logtarget, 'maxlevel') and level > logtarget.maxlevel):continue
                result=logtarget.log(messageold)

    def clear(self):
        self.logs=[]

    def close(self):
        #for old logtargets
        for logtarget in self.logTargets:
            logtarget.close()

    def cleanup(self):
        """
        Cleanup your logs
        """
        if hasattr(self, '_fallbackLogger') and hasattr(self._fallbackLogger, 'cleanup'):
            self._fallbackLogger.cleanup()

        for logtarget in self.logTargets:
            if hasattr(logtarget, 'cleanup'):
                logtarget.cleanup()



    #@deprecated('q.logger.cleanupLogsOnFilesystem', 'q.logger.cleanup', '4.0')
    def cleanupLogsOnFilesystem(self):
        """
        cleanup all old logfiles
        """
        self.cleanup()



#####OLD CODE, WILL BE OBSOLETED ONCE NEW INFRASTRUCTURE WORKS

    def _encodeLog(self, message, level=5, logtype=1, source='', tags=''):
        """
        format of log message see: http://bitbucket.org/despiegk/ssospecs/src/tip/1.1/concepts/EventManagement/1. pylabsLogEventMgmt.wiki
        @return string
        """
        now = time.time()
        source = source.strip().replace("\r\n", "/n").replace("\n", "/n").replace("|","/|").replace(":","/:")
        message = str(message).strip().replace("\r\n", "/n").replace("\n", "/n").replace("|","/|").replace(":","/:")
        tags = str(tags).strip().replace("\r\n", "/n").replace("\n", "/n").replace("|","/|")
        return '%s|%s|%s|%d|%s|%s'%(logtype, now, source, level, tags, message)

    def logTargetAdd(self, logtarget):
        """
        Add a LogTarget object
        """
        count = self.logTargets.count(logtarget)
        if count > 0:
            return
        self.logTargets.append(logtarget)

