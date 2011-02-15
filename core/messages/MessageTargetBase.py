#import pylabs
import pprint
from pylabs.Shell import *
from pylabs.messages.MessageObject import MessageObject
from pylabs import q

class MessageTargetBase(object):
    
    def __init__(self):
        """
        """
        self.enabled = True
        self.name="stdout"
        self._types={} #list of types enabled to send to stdout and value is levels enabled
        self.enableMessageType(q.enumerators.MessageType.LOG)
        self.enableMessageType(q.enumerators.MessageType.ERRORCONDITION)
        self.enableMessageType(q.enumerators.MessageType.JOB)
        #self.enableMessageType(q.enumerators.MessageType.PYMODEL)
        self.enableMessageType(q.enumerators.MessageType.RPC)
        self.enableMessageType(q.enumerators.MessageType.UNKNOWN)
        self.enableMessageType(q.enumerators.MessageType.TESTRESULT)

    def enableMessageType(self, messagetype,levels=[0,1,2,3,4,5]):
        q.enumerators.MessageType.check(messagetype)
        self._types[messagetype]=levels
        
    def checkTarget(self):
        """
        check status of target, if ok return True
        for std out always True
        """
        return True
    
    def sendmessage(self, message,exchange):
        """
        """    
        if not isinstance(message,MessageObject):
            raise RuntimeError("Message needs to be of type messageobject")
        #ipshell()
        if message.level in self._types[message.mtype] and self._types.has_key(message.mtype):
            self._sendmessage(message,exchange)
            
    def _sendmessage(self, message,exchange):
        q.console.echo(self.formatter(message))            
        
    def formatter(self,message):
        return str(message)
        
    def __eq__(self, other):
        if not other:
            return False
        if not isinstance(other, LogTargetStdOut):
            return False        
        return True
    
    def close(self):
        pass
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return __str__(self)
