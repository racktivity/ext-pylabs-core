import time
import traceback
from pymonkey import q, i
from MessageObject import MessageObject
from pymonkey.Shell import *
import string

class ErrorconditionObject(MessageObject):
    
    def clearBacktrace( self ) :
        self.backtrace = ""
        self.backtraceextra = ""
        
    def clearLogging( self ) :
        self.logs = []
         
    def __init__(self,messagestr=""):
        MessageObject.__init__(self,messagestr)
        self.mtype = q.enumerators.MessageType.ERRORCONDITION
        self.logs=[]
        self.errormessagepublic= ""
        self.errormessageprivate = ""
        self.backtrace =""
        self.backtraceextra=""
        self.typeid=""
        self.transactionsinfo=""
        if messagestr<>"":
            self._fromString(messagestr)
            self.bodyDecode()

    def initNoBacktrace(self, message, messageprivate='', level=q.enumerators.ErrorconditionLevel.ERROR, typeid='', tags=''):
        """
        this object represents an errorcondition but no python traceback or logs or transactions are used
        """
        if tags<>"":
            self.tags = tags
        self.errormessagepublic= message
        self.errormessageprivate = messageprivate
        self.level = level or q.enumerators.ErrorconditionLevel.CRITICAL
        self.level = int(self.level)
        self.typeid = typeid
        self.bodyEncode()            
            
    def init(self, message, messageprivate='', level=q.enumerators.ErrorconditionLevel.ERROR, typeid='', tags='', tb='',backtracebasic=""):
        """
        this object represents an errorcondition
        @param tb = backtrace to give context to self.getStackFrameLog()
        """
        if tags<>"":
            self.tags = tags
        self.errormessagepublic= message
        self.errormessageprivate = messageprivate
        self.level = level or q.enumerators.ErrorconditionLevel.CRITICAL
        self.level = int(self.level)
        self.typeid = typeid

        self.backtraceextra=self.getBacktraceDetailed(tb).strip()
        if backtracebasic=="":
            self.backtrace=self.getBacktrace().strip()
        else:
            self.backtrace=backtracebasic

        if q.transaction.activeTransaction<>None:
            self.transactionsinfo="\n%s"%(string.join([transaction.getErrorMessage(True) for transaction in q.transaction.transactions],"\n"))

        if len(q.logger.logs)>0:
            self.logs=q.logger.logs
            q.logger.clear()
        self.bodyEncode()

    def escalate(self):
        """
        escalate errorcondition through filesystem & messagehandlers
        """
        result=self._str(reverse=False,logs=True,backtrace=True)
        q.system.fs.createDir(q.system.fs.joinPaths(q.dirs.logDir,"errors",q.application.appname))
        path=q.system.fs.joinPaths(q.dirs.logDir,"errors",q.application.appname,"backtrace_%s.log"%(q.base.time.getLocalTimeHRForFilesystem()))
        q.system.fs.writeFile(path,result)

        return path

    def getBacktrace(self):
        stack=""
        for x in traceback.format_stack():
            ignore=False
            #if x.find("IPython")<>-1 or x.find("MessageHandler")<>-1 \
            #   or x.find("EventHandler")<>-1 or x.find("ErrorconditionObject")<>-1 \
            #   or x.find("traceback.format")<>-1 or x.find("ipython console")<>-1:
            #    ignore=True
            stack = "%s"%(stack+x if not ignore else stack)
        return stack

    def bodyEncode(self):
        """
        properties errormessagepublic & errormessageprivate & backtrace & logs are encoded to proper body
        """
        self.backtrace=str(self.backtrace).strip()
        self.errormessageprivate=str(self.errormessageprivate).strip()
        self.errormessagepublic=str(self.errormessagepublic).strip()
        self.transactionsinfo=str(self.transactionsinfo).strip()
        self.typeif=str(self.typeid).strip()
        self.body=self._str(reverse=False,logs=True,backtrace=True,machinereadable=True)
        self.body=self.body.strip()


    def bodyDecode(self):
        """
        decode body to properties: errormessagepublic & errormessageprivate & backtrace & logs
        """
        self.body=self.body.strip()
        splitted=self.body.split("*#***")
        def findItem(splitted,tofind):
            value=""
            for t in range(len(splitted)):
                if splitted[t].find(tofind)==0:
                    #found item, next line is value we are looking for
                    pos=splitted[t+1].find("******-*")
                    if pos<>-1:
                        value=splitted[t+1][pos+8:]
                    else:
                        raise RuntimeError("error in decoding of errorcondition.body, not expected format %s" % self.body)
            return value
        self.errormessagepublic=findItem(splitted,"public").strip()
        self.errormessageprivate=findItem(splitted,"private").strip()
        self.backtrace=findItem(splitted,"backtrace").strip()
        self.backtraceextra=findItem(splitted,"backtraceextra").strip()
        self.transactionsinfo=findItem(splitted,"transactions").strip()
        self.typeid = findItem(splitted, "typeid").strip()
        logstrsplitted=findItem(splitted,"logs").strip().split("\n")
        self.logs=[ q.messagehandler.getLogObject(logstr) for logstr in logstrsplitted]

        ##count=self.body.count(q.errorconditionhandler._sep)
        ##if count==0:
            ##raise RuntimeError("Cannot split body of message to become errorcondition object, no separation lines.\n%s" % self.body)
        ##splitted=self.body.split(q.errorconditionhandler._sep)
        ##if count==1:
            ##self.errormessagepublic=splitted[0]
            ##self.logs=splitted[1].split("\n")
        ##elif count == 2:
            ##self.backtrace=splitted[0]
            ##self.errormessagepublic=splitted[1]
            ##self.logs=splitted[2].split("\n")
        ##elif count == 3:
            ##self.backtrace=splitted[0]
            ##self.errormessageprivate=splitted[1]
            ##self.errormessagepublic=splitted[2]
            ##self.logs=splitted[3].split("\n")
        ##else:
            ##raise RuntimeError("Cannot split body of message to become errorcondition object.\n%s" % self.body)

    def _filterLocals(self,k,v):
        try:
            k="%s"%k
            v="%s"%v
            if k in ["re","q","pymonkey","pprint","qexec","qshell","Shell","__doc__","__file__","__name__","__package__","i","main","page"]:
                return False
            if v.find("<module")<>-1:
                return False
            if v.find("IPython")<>-1:
                return False
            if v.find("<built-in function")<>-1:
                return False
            if v.find("pymonkey.Shell")<>-1:
                return False
        except:
            return False

        return True

    def getBacktraceDetailed(self,tracebackObject=""):
        """
        Get stackframe log
        is a very detailed log with filepaths, code locations & global vars, this output can become quite big
        """
        sep="\n"+"-"*90+"\n"
        result = ''
        if not tracebackObject:
            return "" #@todo needs to be fixed so it does work
        if tracebackObject==None:
            tracebackObject = inspect.currentframe()  #@todo does not work
        frames = inspect.getinnerframes(tracebackObject, 16)
        for (frame, filename, lineno, fun, context, idx) in frames:
            ##result = result + "-"*50 + "\n\n"
            location=filename + "(line %d) (function %s)\n" % (lineno, fun)
            if location.find("EventHandler.py")==-1:
                result += "  " + sep
                result += "  " + location
                result += "  " + "========== STACKFRAME==========\n"
                if context:
                    l = 0
                    for line in context:
                        prefix = "    "
                        if l == idx:
                            prefix = "--> "
                        l += 1
                        result += prefix + line
                result += "  " + "============ LOCALS============\n"
                for (k,v) in sorted(frame.f_locals.iteritems()):
                    if self._filterLocals(k,v):
                        try:
                            result += "    %s : %s\n" % (str(k), str(v))
                        except:
                            pass
                ##result += "  " + "============ GLOBALS============\n"
                ##for (k,v) in sorted(frame.f_globals.iteritems()):
                ##    if self._filterLocals(k,v):
                ##        result += "    %s : %s\n" % (str(k), str(v))
        return result

    def __str__(self):
        """
        nice formatting of event, human readable
        """
        return self._str(reverse=True)

    def _str(self,reverse=False,logs=False,backtrace=False,machinereadable=False):
        if machinereadable:
            width=50
        else:
            width=120
        def getsep(topic,width=width,machinereadable=machinereadable):
            """
            getseparator
            """
            if machinereadable:
                return "\n*#***%s***#*%s-*\n" % (topic,"*"*(width-8-len(topic)))
            else:
                return "\n\n****%s****%s\n" % (topic,"*"*(width-8-len(topic)))
        infoarray=[]
        if machinereadable==False:
            infoarray.append("\ntype:%s time:%s level:%s agent:%s application:%s tags:%s" % \
             (self.mtype,\
              q.base.time.epoch2HRDateTime(self.timestamp),\
              self.level,\
              self.agent,\
              self.application,\
              self._strEncode(self.tags)\
              ))
        infoarray.append(getsep("public")+self.errormessagepublic)
        if self.errormessageprivate<>"":
            infoarray.append(getsep("private")+self.errormessageprivate)
        if self.transactionsinfo<>"":
            infoarray.append(getsep("transactions")+self.transactionsinfo)
        if self.backtrace<>"":
            infoarray.append(getsep("backtrace")+self.backtrace)
        if self.typeid:
            infoarray.append("%s%s" % (getsep("typeid"), self.typeid))
        if logs and len(self.logs)>0:
            self.logs=[log for log in self.logs if log.timestamp>q.base.time.getTimeEpoch()-60*15] #ignore everything older than 15 minutes
            if len(self.logs)>500: #make sure not more than 500 logs
                self.logs=self.logs[-500:]
            if machinereadable==False:
                logs=string.join([log._strshort() for log in self.logs],"\n")
            else:
                logs=string.join([log.getMessageString(multiline=False) for log in self.logs],"\n")
            infoarray.append(getsep("logs")+logs)
        if self.backtraceextra<>"" and backtrace:
            if len(self.backtraceextra)>500*1024: #more than 500kb
                self.backtraceextra=self.backtraceextra[:500*1024]
                self.backtraceextra+="\n....BACKTRACE TOO BIG, LIMITED TO 500KB\n"
            infoarray.append(getsep("backtraceextra")+self.backtraceextra)
        if reverse:
            infoarray.reverse()
        msg=string.join(infoarray,"")
        return msg

    __repr__ = __str__
