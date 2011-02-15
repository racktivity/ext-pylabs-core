#import pylabs
from pylabs import q
import pprint
from pylabs.Shell import *
from pylabs.messages.MessageObject import MessageObject
from MessageTargetBase import MessageTargetBase

class QueueXMPP(MessageTargetBase):
    
    def __init__(self):
        """
        self.servers=[]  array of xmpp servers
        self.login=""
        self.passwd=""
        self.exchangenames=[] is array if exchangenames which are enabled in this queue, if [] then all
        """
        MessageTargetBase.__init__(self)
        self.name="qxmpp"
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
        q.console.echo("XMPP QUEUE: " +self.formatter(message))
        #@todo implement
        
    def formatter(self,message):
        return str(message)
        
