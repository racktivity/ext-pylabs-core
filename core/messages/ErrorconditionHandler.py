import traceback
import sys, os
#import pylabs
from pylabs import q
from pylabs.messages import toolStripNonAsciFromText

from pylabs.messages.ErrorconditionObject import ErrorconditionObject
from pylabs.messages.ErrorConditionType import ErrorConditionTypeFactory
from pylabs.Shell import *

class ErrorconditionHandler():
    '''
    The EventHandler class catches errors, messages or warnings and
    processes them
    '''
    def __init__(self):
        sys.excepthook = self._exceptionhook
        self._sep="*-***********************-*" #separater used in encoding/decoding to messages
        self.lastErrorconditionObject=None
        self.lastErrConTimes = dict()
        self.lastErrConMessages = dict()
        self.lastErrConTags = dict()


    def _raise(self, message, messageprivate='', level=None, typeid='', tags='', backtrace=None, escalate=False):
        """
        @param message: is public message which can be shown to end users
        @type message: string
        @param messageprivate: is private error message which will not be shows to end users
        @type messageprivate: string
        @param level: the ErrorconditionLevel
        @type level: int
        @param typeid: Event type identifier
        @type typeid: string        
        @param tags: (see q.tags... to construct a tagstring)
        @type tags: string
        @param backtrace: is free text describing the source, if not filled in will be automatically filled in with applicationname
        @type backtrace: string
        @param escalate: escalate event
        @type escalate: bool
        """

        message=toolStripNonAsciFromText(message)
        messageprivate=toolStripNonAsciFromText(messageprivate)
        
        if messageprivate<>"":
            errormessage="%s\n%s" % (message, messageprivate)
        else:
            errormessage=message
            
        self._dealWithRunningAction()

        if escalate:
            self._escalateEvent(message, messageprivate, level, typeid, tags, backtrace)
        
        if int(level) <= 3:
            raise Exception(errormessage)
        else:
            q.logger.log(errormessage, level,3)

    def _getEscalationParamDict(self, errConObj):
        
        source= q.application.agentid+"_"+q.application.appname
        
        params = dict()
        params[ "messageobject"] = errConObj
        params[ "source" ] = source
        
        errConType = ErrorConditionTypeFactory.getType ( errConObj.typeid )
        if errConType is not None :
            params.update( errConType.getEscalationParamDict() )
            if len ( params ) != 0 :
                params[ "lastErrorConditionTimestamps" ] = self.lastErrConTimes
                params[ "lastErrorConditionMessages" ] = self.lastErrConMessages
                params[ "lastErrorConditionTags" ] = self.lastErrConTags
        return params


    def raiseCritical(self, message, messageprivate="", typeid="", tags="", escalate=False):
        self._raise(message, messageprivate, q.enumerators.ErrorconditionLevel.CRITICAL, typeid, tags, escalate=escalate)


    def raiseUrgent(self, message, messageprivate="", typeid="", tags="", escalate=False):
        self._raise(message, messageprivate, q.enumerators.ErrorconditionLevel.URGENT, typeid, tags, escalate=escalate)


    def raiseWarning(self, message, messageprivate="", typeid="", tags="", escalate=False):
        self._raise(message, messageprivate, q.enumerators.ErrorconditionLevel.WARNING, typeid, tags, escalate=escalate)


    def raiseInfo(self, message, messageprivate="", typeid="", tags="", escalate=False):
        self._raise(message, messageprivate, q.enumerators.ErrorconditionLevel.INFO, typeid, tags, escalate=escalate)

    def raiseError(self, message, messageprivate="", typeid="", tags="", escalate=False):
        self._raise(message, messageprivate, q.enumerators.ErrorconditionLevel.ERROR, typeid, tags, escalate=escalate)

    def escalateEvent(self, message='', messageprivate='', level=None, typeid='', tags='', backtrace=None):
        """
        @param message: is public message which can be shown to end users
        @type message: string
        @param messageprivate: is private error message which will not be shows to end users
        @type messageprivate: string
        @param level: the ErrorconditionLevel level
        @type level: int
        @param typeid: Event type identifier
        @type typeid: string        
        @param tags: (see q.tags... to construct a tagstring)
        @type tags: string
        @param backtrace: is free text describing the source, if not filled in will be automatically filled in with applicationname
        @type backtrace: string
        """
        
        message=toolStripNonAsciFromText(message)
        messageprivate=toolStripNonAsciFromText(messageprivate)
        
        if messageprivate<>"":
            errormessage="%s\n%s" % (message, messageprivate)
        else:
            errormessage=message
        
        self._escalateEvent(message, messageprivate, level, typeid, tags, backtrace)

    def _escalateEvent(self, message, messageprivate='', level=None, typeid='', tags='', backtrace=None):
        """
        @param message: is public message which can be shown to end users
        @type message: string
        @param messageprivate: is private error message which will not be shows to end users
        @type messageprivate: string
        @param level: the ErrorconditionLevel level
        @type level: int
        @param typeid: Event type identifier
        @type typeid: string        
        @param tags: (see q.tags... to construct a tagstring)
        @type tags: string
        @param backtrace: is free text describing the source, if not filled in will be automatically filled in with applicationname
        @type backtrace: string
        """
        
        errConType = ErrorConditionTypeFactory.getType(typeid)
        
        solution = ""
        if errConType is not None:
            solution = errConType.definition.solution
            if len(solution) > 0 :
                messageprivate = "%sPossible solution:\n%s" % ('%s\n'%messageprivate if messageprivate else '', solution)

        # Build params for the error condition type
        try :
            errConObj = ErrorconditionObject()
                 
            errConObj.init(message, messageprivate, level, typeid, tags, backtrace)

            params = self._getEscalationParamDict(errConObj )
                            
            if len(params) > 0 :        
                q.messagehandler.sendMessage(errConObj, params)
                
        except Exception, ex:
            q.logger.log( "Error condition escalation failed. (%s: '%s')" % (ex.__class__.__name__, ex) , 1)
        
        
            

    def _exceptionhook(self, ttype, errorObject, tb, stop=True):
        """ every fatal error in pylabs or by python itself will result in an exception
        in this function the exception is caught.
        @ttype : is the description of the error
        @tb : can be a python data object or a Event
        """
        message = "%s %s %s" % (ttype, errorObject, tb)

        self._dealWithRunningAction()

        #if isinstance(errorObject, Exception):
        backtrace = "~ ".join([res for res in traceback.format_exception(ttype, errorObject, tb)])

        eobject=ErrorconditionObject()

        eobject.init(message=message, messageprivate='', level=q.enumerators.ErrorconditionLevel.CRITICAL, typeid='', tags='', tb=tb,backtracebasic=backtrace)

        tracefile=eobject.escalate()
        params = self._getEscalationParamDict( eobject )
        q.messagehandler.sendMessage(eobject, params)
        self.lastErrorconditionObject=eobject

        if q.qshellconfig.interactive:
            q.logger.log("***ERRORTRACEBACK***\n%s\n********************\n" % (backtrace) , 2)
            q.logger.log("\n***ERROR*** %s\n%s\n" % (ttype,message), 1)

            q.logger.log("\nDetailed logs, stacktrace & locals can be found at %s\n" % tracefile,1)

            try:
                res=q.gui.dialog.askString("\nERROR HAPPENED, do you want the application to stop or continue (s=stop)(t=getTrace)")
            except:
                res="s"
            if res=="t":                
                if q.platform.isLinux():
                    q.console.echo("THIS ONLY WORKS WHEN GEDIT IS INSTALLED")
                    result,out=q.system.process.execute("gedit %s 2>&1 > /dev/null &" % tracefile,dieOnNonZeroExitCode=False, outputToStdout=False)
                if q.platform.isWindows():
                    scitecmd=q.system.fs.joinPaths(q.dirs.baseDir,"apps","wscite","scite.exe")
                    if not q.system.fs.exists(scitecmd):
                        q.console.echo( "Cannot find scite, cannot show tracelog, please install newest qbase sandbox on windows")
                    else:
                        result,out=q.system.process.execute("%s %s" % (scitecmd,tracefile),dieOnNonZeroExitCode=False, outputToStdout=False)
                q.logger.clear()

            if res=="s":
                q.application.stop(1)
        else:
            self._raise(message, level=q.enumerators.ErrorconditionLevel.CRITICAL, backtrace=backtrace )

    def __exceptionhook(self, ttype, errorObject, tb,stop=True):
        """
        every fatal error in pylabs or by python itself will result in an exception
        in this function the exception is caught.
        """

        ttype="%s" % type(errorObject)
        if ttype.find("exception")=="":
            q.logger.log("ERROR: exception raised is not of type exception, this is a bug in exception handling procedures",2)
            errormessage="%s" % errorObject
        else:
            ttype=ttype.split(".")[1]
            ttype=ttype.split("'")[0]

            if len(errorObject.args) > 0:
                errormessage = errorObject.args[0]
            else:
                errormessage = ''
            ##source = q.application.appname
        #if you want to call original exceptionhook
        ##sys.__excepthook__(ttype, value,tb)

        #create errorcondition message
        eobject=ErrorconditionObject()
        backtracebasic="~ ".join([res for res in traceback.format_exception(ttype, errorObject, tb)])
        eobject.init(message=errormessage, messageprivate='', level=q.enumerators.ErrorconditionLevel.CRITICAL, typeid='', tags='', tb=tb,backtracebasic=backtracebasic)
        tracefile=eobject.escalate()
        q.messagehandler.sendMessage(eobject)
        self.lastErrorconditionObject=eobject

        #@todo , next will be no longer needed when above is working fine, for now leave it in
        source=""
        logmsg1="\n***ERROR*** %s\n%s\n" % (ttype,errormessage)
        logmsg5="***ERRORTRACEBACK***\n%s\n********************\n" % (backtracebasic)
        q.logger.log(logmsg5,2)
        q.logger.log(logmsg1,1)


        if q.qshellconfig.interactive<>True and stop==True:
            q.logger.log("\nDetailed logs, stacktrace & locals can be found at %s\n" % tracefile,1)
            q.application.stop(1)
        elif stop==False:
            return False
        else:
            if q.qshellconfig.interactive:
                q.logger.log("\nDetailed logs, stacktrace & locals can be found at %s\n" % tracefile,1)

                try:
                    res=q.gui.dialog.askString("\nERROR HAPPENED, do you want the application to stop or continue (s=stop)(t=getTrace)")
                except:
                    res="s"
                if res=="t":
                    q.console.echo("THIS ONLY WORKS WHEN GEDIT IS INSTALLED")
                    result,out=q.system.process.execute("gedit %s 2>&1 > /dev/null &" % tracefile,dieOnNonZeroExitCode=False, outputToStdout=False)
                    #result=q.system.process.executeWithoutPipe("ggedit %s" % tracefile,printCommandToStdout=False, outputToStdout=False)
                    #result,out=q.system.process.executeWithoutPipe("gedit %s --new-document 2>&1 > /dev/null &" % tracefile,dieOnNonZeroExitCode=False, outputToStdout=False)
                    #q.system.process.executeAsync("gedit %s" % tracefile, printCommandToStdout = False, outputToStdout=False)
                    #ipshell()
                    q.logger.clear()
                if res=="s":
                    q.application.stop(1)

            return()


    def _dealWithRunningAction(self):
        """Function that deals with the error/resolution messages generated by q.action.start() and q.action.stop()
        such that when an action fails it throws a pylabs event and is directed to be handled here
        """
        if q.action.hasRunningActions():
            q.console.echo("\n\n")
            q.action.printOutput()
            q.console.echo("\n\n")
            q.console.echo( "ERROR:\n%s\n" % q.action._runningActions[-1].errorMessage)
            q.console.echo( "RESOLUTION:\n%s\n" % q.action._runningActions[-1].resolutionMessage)
            q.action.clean()

    def getCurrentExceptionString(self, header = None):
        """ Get description on exception currently being handled """
        if (header == None or header == ""):
            result = ""
        else:
            result = header + "\n"

        e1, e2, e3 = sys.exc_info()
        for x in traceback.format_exception(e1, e2, e3):
            result = result + x

        return result



