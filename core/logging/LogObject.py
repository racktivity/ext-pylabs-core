from pymonkey.logging.EventObject import EventObject
from LogTypes import LogType
from pymonkey import q
from collections import defaultdict


class LogObject(object):
    """
    developper friendly representation of log message, DO NOT USE TO LOG ONLY FOR REPRESENTATION 
    """
    
    def __init__(self, logMessageString):
        """
        Initialize a logging object starting from a log string
        """        
        self.type = int(LogType.LOG) 
        self.source = ''
        self.message = ''
        self.tagsString = ''
        self.tagsDict = defaultdict(lambda: '')
        self.tagswithvalues = list()
        self.labels = list()
        self.isevent = False
        self.level = 7
        if logMessageString:
            self.fromString(logMessageString)
            
    def fromString(self, logMessageString):    
        try:
            logMessageString = logMessageString.replace('/|', '@@')            
            self.type, self.timestamp, self.source, self.level, self.tags, self.message = logMessageString.split('|')
            self.type = int(self.type)
            self.level = int(self.level) 
            self.source = self.source.strip().replace("/n", "\n").replace("@@","|").replace("/:",":")
            self.message = self.message.strip().replace("/n", "\n").replace("@@","|").replace("/:",":")
            self.tags = self.tags.strip().replace("/n", "\n").replace("@@","|")#note that originally we didn't encode the colon in the tags
        except:
            msg="Could not decode log message, nr of | in message is not correct./n%s" % logMessageString
            q.console.echo(msg) #also send to stdout, can become ugly if bug in loghandler
            raise RuntimeError(msg)        
    
        
              
    def getTagObject(self):
        """
        use q.base.tags... to return tagobject
        """
        return q.base.tags.getObject(self.tags)
        
    def getEventObject(self):
        """
        converts a log object into event object if applicable
        """
        return EventObject.fromLog(self)
        

    def __str__(self):
        """
        nice formatting of log
        detect if event if event transform to event and print as event
        """
        if self.type == int(LogType.EVENT):
            return str(self.getEventObject())
        
        return str(self.message)