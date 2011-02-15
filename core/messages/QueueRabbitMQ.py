#import pylabs
import pprint
from pylabs.Shell import *
from pylabs.messages.MessageObject import MessageObject
from MessageTargetBase import MessageTargetBase
from pylabs import q

class QueueRabbitMQ(MessageTargetBase):
    
    def __init__(self):
        """
        """
        MessageTargetBase.__init__(self)
        self.name="qrabbitmq"
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
        q.console.echo("RABBITMQ QUEUE: " +self.formatter(message))
        #@todo implement
        
    def formatter(self,message):
        return str(message)
        
