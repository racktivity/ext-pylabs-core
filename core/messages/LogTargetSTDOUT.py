#import pymonkey
import pprint
from pymonkey.Shell import *
from pymonkey.messages.MessageObject import MessageObject
from MessageTargetBase import MessageTargetBase
from pymonkey import q

#@todo question, please let despiegk know why we have this object and where and how it is being used, what is relation with LogObject? Seems to be in wrong location.

class LogTargetSTDOUT(MessageTargetBase):
    
    def __init__(self):
        """
        """
        MessageTargetBase.__init__(self)
        self.ejabberdservers=[]
        self.login=""
        self.passwd=""
        #self.enableMessageType(q.enumerators.MessageType.LOG)
        #self.enableMessageType(q.enumerators.MessageType.ERRORCONDITION)
        #self.enableMessageType(q.enumerators.MessageType.JOB)
        #self.enableMessageType(q.enumerators.MessageType.PYMODEL)
        #self.enableMessageType(q.enumerators.MessageType.RPC)
        #self.enableMessageType(q.enumerators.MessageType.UNKNOWN)
        #self.enableMessageType(q.enumerators.MessageType.TESTRESULT)  
            
    def _sendmessage(self, message,exchange=""):
        q.console.echo(self.formatter(message))
        
    def formatter(self,message):
        return str(message)
        
