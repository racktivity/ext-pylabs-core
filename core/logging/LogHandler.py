import time
import pymonkey
from pymonkey.Shell import *
from logtargets.LogTargetFS import LogTargetFS
from pymonkey.logging.LogConsoleController import LogConsoleController

try:
    from pymonkey.logging.logtargets.LogTargetScribe import LogTargetScribe
except ImportError:
    pass

from pymonkey.logging.logtargets.LogTargetToPylabsLogConsole import LogTargetToPylabsLogConsole
from pymonkey.messages import toolStripNonAsciFromText
from pymonkey.messages.LogObject import LogObject
from pymonkey.decorators import deprecated

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
        inifile=pymonkey.q.config.getInifile("main")
        if inifile.checkParam("main","lastlogcleanup")==False:
            inifile.setParam("main","lastlogcleanup",0)
        self._lastcleanuptime=int(inifile.getValue("main","lastlogcleanup"))
        self.nolog=False
        self.logTargetAdd(LogTargetToPylabsLogConsole())
        try:
            self.logTargetAdd(LogTargetScribe())
        except:
            pymonkey.q.logger.log("Could not add logtarget scribe")


    def _inittargets(self):
        """
        only execute this every 5 secs
        """
        if self._lastinittime<pymonkey.q.base.time.getTimeEpoch()-5:
            
            #check which loggers are not working
            for target in self.logTargets:
                if target.enabled==False:
                    try:
                        target.open()
                    except:
                        target.enabled = False
            self.cleanupLogsOnFilesystem()
            self._lastinittime=pymonkey.q.base.time.getTimeEpoch()
            

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
            pymonkey.q.console.echo(message,log=False)
        if self.nolog:
            return
        #if message<>"" and message[-1]<>"\n":
        #    message+="\n"
        if level<self.maxlevel+1:
    
            #print pymonkey.q.application.state
            #if pymonkey.q.application.state==pymonkey.q.enumerators.AppStatusType.RUNNING:
            logobject=LogObject()
            logobject.init(message,level,tags)
            
            #add to active transaction when there is one
            if pymonkey.q.transaction.activeTransaction<>None:
                if len (pymonkey.q.transaction.activeTransaction.logs)>250:
                    pymonkey.q.transaction.activeTransaction.logs=pymonkey.q.transaction.activeTransaction.logs[-200:]
                pymonkey.q.transaction.activeTransaction.logs.append(logobject)
                
            self.logs.append(logobject)
            if len (self.logs)>550:
                    self.logs=self.logs[-500:]

            #log to old logtargets
            source= pymonkey.q.application.agentid+"_"+pymonkey.q.application.appname
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

