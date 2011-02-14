#import pymonkey
from pymonkey import q
#from collections import defaultdict
from pymonkey.Shell import *

class MessageObject():
    """
    developper friendly representation of pylabs message
    """

    def __init__(self, messagestr=""):
        """
        Initialize a logging object starting from a log string
        """
        self.mtype = q.enumerators.MessageType.UNKNOWN
        self.timestamp=0
        self.level =0
        self.agent= q.application.agentid
        self.application = q.application.appname
        self.body = ''
        self.tags = ''
        self.returnqueue=''

        if messagestr<>"":
            self._fromString(messagestr)
        else:
            self.timestamp=q.base.time.getTimeEpoch()
            self.agent= q.application.agentid
            self.application = q.application.appname
            try:
                self.taghandler=q.base.tags.getObject(self.tags)
            except:
                pass

    def getMessageString(self,multiline=False):
        #construct the message string out of the properties
        def check(txt):
            if txt.find("|")<>-1 or txt.find(":")<>-1 or txt.find("\n")<>-1 :
                self._trapError("Found forbidden chars in tags, agent & application part.\n%s" % txt)
            return txt
        if multiline==False:
            messagestr="%s|%s|%s|%s|%s|%s|%s|%s" % (int(self.mtype),\
                int(self.timestamp),\
                int(self.level),\
                check(self.agent),\
                check(self.returnqueue),\
                self._strEncode(self.application),\
                self._strEncode(self.tags),\
                self._strEncode(self.body)\
                )
        else:
            messagestr="%s|%s|%s|%s|%s|%s|%s|\n%s" % (int(self.mtype),\
                int(self.timestamp),\
                int(self.level),\
                check(self.agent),\
                check(self.returnqueue),\
                self._strEncode(self.application),\
                self._strEncode(self.tags),\
                self._strEncode(self.body,True)\
                )
        return messagestr


    def _mtypeFromInt(self,nr):
        nr=int(nr)
        return q.enumerators.MessageType.getByLevel(nr)

    def _fromString(self, messageString):
        messageString=messageString.replace("/n","\n")
        bodyString=messageString.replace("/|","@#$")
        if bodyString.count("|")<>7:
            self._trapError("messageString is not properly formatted.\n%s" % bodyString)
        mtype, self.timestamp, level,self.agent, self.returnqueue,self.application,tags, self.body = bodyString.split('|')
        self.mtype = self._mtypeFromInt(int(mtype))
        self.timestamp = int(self.timestamp)
        ###level is different depending type
        self.level=int(level)
        self.level = int(self.level)
        self.application = self._strDecode(self.application)
        self.body = self._strDecode(self.body)
        self.tags = self._strDecode(tags).replace("/:",":")
        self.taghandler=q.base.tags.getObject(self.tags)

    def getLevelAsEnumerator(self):
        if self.mtype==q.enumerators.MessageType.LOG:
            return q.enumerators.LogLevel.getByLevel(level)
        elif self.mtype==q.enumerators.MessageType.LOG:
            return q.enumerators.ErrorconditionLevel.getByLevel(level)
        else:
            raise RuntimeError("Cannot find enumerator level for messages with type %s" % self.mtype)

    def _strDecode(self,sstring):
        sstring=sstring.replace("\t","    ").replace("\r","")
        return sstring.strip().replace("/n", "\n").replace("@#$","|").replace("/|","|")

    def _strEncode(self,sstring,multiline=False):
        sstring=str(sstring)
        sstring=sstring.replace("\t","    ").replace("\r","")
        sstring=sstring.strip().replace("|","/|")
        if multiline==False:
            sstring=sstring.replace("\n", "/n")
        return sstring

    def _trapError(self,msg):
        raise RuntimeError("%s\nSee http://www.pylabs.org/display/PM/MessageFormat" % (msg))

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
        return messagestr
