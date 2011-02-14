#import pymonkey
from pymonkey import q
import pprint
from pymonkey.Shell import *
from pymonkey.messages.MessageObject import MessageObject
from MessageTargetBase import MessageTargetBase

class QueueZookeeper(MessageTargetBase):
    
    def __init__(self):
        """
        """
        MessageTargetBase.__init__(self)
        self.name="qzookeeper"
        self.servers=[]
        self.login=""
        self.passwd=""
        self.exchangenames=[]        
        #self.enableMessageType(q.enumerators.MessageType.LOG)
        #self.enableMessageType(q.enumerators.MessageType.ERRORCONDITION)
        #self.enableMessageType(q.enumerators.MessageType.JOB)
        #self.enableMessageType(q.enumerators.MessageType.PYMODEL)
        #self.enableMessageType(q.enumerators.MessageType.RPC)
        #self.enableMessageType(q.enumerators.MessageType.UNKNOWN)
        #self.enableMessageType(q.enumerators.MessageType.TESTRESULT)
            
    def _sendmessage(self, message,exchange):
        q.console.echo("ZOOKEEPER QUEUE: " + self.formatter(message))
        #@todo implement
        
    def formatter(self,message):
        return str(message)
        
