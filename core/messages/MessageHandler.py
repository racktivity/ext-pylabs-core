import os
from pylabs import q
from pylabs.taskletengine.TaskletEngine4 import TaskletEngine4

class MessageHandler(object):
    """
    Message Handler class
    """

    def __init__(self):
        taskletsDir = q.system.fs.joinPaths(q.dirs.appDir, 'pylabs_messagehandler', 'tasklets')
        if not q.system.fs.exists(taskletsDir): q.system.fs.createDir(taskletsDir)
        try:
            self._engine = TaskletEngine4(taskletsDir)
            self._tasklets_loaded = True
        except Exception as ex:
            self._tasklets_loaded = False

    
    def sendMessage(self, messageObject, params=None):
        """
        Execute tasklets matching the type of the message object e.g. log, errorcondition
        @param messageObject: MessageObject object
        """
        if not self._tasklets_loaded:
            try:
                self._engine._reload()
                self._tasklets_loaded = True
            except:
                return False

        def wrapper(func):
            def main(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    q.logger.log("Failed to execute tasklet. (%s: %s) :"% (ex.__class__.__name__, ex) , 6)
            return main

        if params is None :
            params = {'messageobject':messageObject}
            
        self._engine.execute(params=params, tags=(str(messageObject.mtype), ), wrapper=wrapper)

    def getMessageObject(self, messagestring=""):
        """
        Return a MessageObject oebject(never used for logging purposes only for review and printing)
        @param messagestring: message
        """
        from pylabs.messages.MessageObject import MessageObject
        return MessageObject(messagestring)

    def getLogObject(self,messagestring=""):
        """
        Return a LogObject
        @param messagestring: message
        """
        from pylabs.messages.LogObject import LogObject
        return LogObject(messagestring)

    def getErrorconditionObject(self,messagestring=""):
        """
        Return a ErrorconditionObject
        @param messagestring: message
        """
        from pylabs.messages.ErrorconditionObject import ErrorconditionObject
        return ErrorconditionObject(messagestring)

    def getRPCMessageObject(self,messagestring=""):
        """
        Return a RPCMessageObject
        @param messagestring: message
        """
        from pylabs.messages.RPCMessageObject import RPCMessageObject
        return RPCMessageObject(messagestring)

#    def getTLogMessageObject(self,messagestring=""):
#        """
#        Return a TLogMessageObject
#        @param messagestring: message
#        """
#        from pylabs.messages.TLogObject import TLogObject
#        return TLogObject(messagestring)    
    
    def getJobMessageObject(self,messagestring=""):
        """
        Return a JobMessageObject
        @param messagestring: message
        """
        from pylabs.messages.JobMessageObject import JobMessageObject
        return JobMessageObject(messagestring)

