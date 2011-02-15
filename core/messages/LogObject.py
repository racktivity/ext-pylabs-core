from pylabs import q
from MessageObject import MessageObject


class LogObject(MessageObject):
    """
    """
    def __init__(self,messagestr=""):
        MessageObject.__init__(self,messagestr)
        self.mtype=q.enumerators.MessageType.LOG

    def init(self,logmsg,loglevel=5,tags="",jobguid=""):
        self.body=logmsg
        self.level=loglevel
        self.jobguid=jobguid
        self.level = int(self.level)
        if tags<>"":
            self.tags=tags

    def getMessageString(self,multiline=False):
        #self.taghandler.tagSet("jobguid",self.jobguid)
        return MessageObject.getMessageString(self,multiline)               
            
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """
        nice formatting message
        """
        #@todo localtime does not work???
        messagestr="type:%s time:%s level:%s agent:%s application:%s tags:%s\n%s" % (self.mtype,\
            q.base.time.epoch2HRDateTime(self.timestamp),\
            self.level,\
            self.agent,\
            self.application,\
            self._strEncode(self.tags),\
            self._strEncode(self.body)\
            )
        return q.console.formatMessage(messagestr,prefix="log",withStar=True,indent=0)

    def _strshort(self):
        """
        nice formatting message
        """
        #@todo localtime does not work???
        messagestr="%s %s" % (q.base.time.epoch2HRTime(self.timestamp),\
            self._strEncode(self.body)\
            )
        return q.console.formatMessage(messagestr,prefix="",withStar=True,indent=0,width=120)
