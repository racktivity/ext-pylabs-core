from pylabs import q
from MessageObject import MessageObject
from pylabs.Shell import *
from pylabs.baseclasses import BaseType
import json

import string

#@todo question, please let despiegk know why we have this object and where and how it is being used, what is relation with LogObject?

class LogMessageObject(MessageObject,BaseType):
    """
    implements http://pylabs.org/display/PM/Log+Message
    """
    #Standard Properties for the logMessageObject
    #logName 
    #logdescription 
    #userErrormsg
    #internalErrormsg
    #loglocation
    #logtimestamp
    #params = model.Dict(model.Object(object), thrift_id=17)

    logname = q.basetype.string(doc="logname",allow_none=False)
    logdescription = q.basetype.string(doc="logdescription",allow_none=False)
    userErrormsg = q.basetype.string(doc="userErrormsg",allow_none=False)
    internalErrormsg = q.basetype.string(doc="internalErrmsg",allow_none=True)
    loglocation = q.basetype.string(doc="loglocation",allow_none=False)
    logtimestamp = q.basetype.string(doc="logtimestamp",allow_none=False)
    params = q.basetype.dictionary(doc="params",allow_none=True)

    def __init__(self,messagestr=""):
        """
        LogMessageObject:Create messagestring for the message type:Log
        """        
        MessageObject.__init__(self,messagestr)
        
        self.params={}
        #Standard Propoerties for the logMessageObject
        #logName 
        #logdescription 
        #userErrormsg
        #internalErrormsg
        #loglocation
        #logtimestamp
        #params = model.Dict(model.Object(object), thrift_id=17)
        if messagestr<>"":
            self._fromString(messagestr)
            self.tagBodyDecode()
        
    def init(self, logname, logdescription, userErrormsg, internalErrormsg, loglocation, logtimestamp, params={}):
        """
        @param tags can be usefull in advanced messaging/queuing scenario's (normally not used)
        """
        self.mtype = q.enumerators.MessageType.LOG        
        self.logname=logname
        self.logdescription=logdescription
        self.userErrormsg=userErrormsg
        self.internalErrormsg=internalErrormsg
        self.loglocation=loglocation
        self.logtimestamp=logtimestamp
        self.params=params               
        self.tagBodyEncode()            
        
    def getMessageString(self):
        self.tagBodyEncode()
        return MessageObject.getMessageString(self)
        
    def tagBodyEncode(self):
        """
        encode custom properties to body & tags of JobMessageObject
        """
        self.body=json.dumps(self.params)
        self.taghandler.tagSet("logname",self.logname)
        self.taghandler.tagSet("logdescription", self.logdescription)
        self.taghandler.tagSet("userErrormsg", self.userErrormsg)
        self.taghandler.tagSet("internalErrormsg", self.internalErrormsg)
        self.taghandler.tagSet("loglocation", self.loglocation)        
        self.taghandler.tagSet("logtimestamp", self.logtimestamp)
        self.taghandler.tagSet("params", self.params)
        #self.body=self.body.strip()
        
        
    def tagBodyDecode(self,tagstring="",body=""):
        """
        decode body & tags to properties
        """
        if body<>"":
            self.body=body
        self.params=json.loads(self.body)
        self.logname=self.taghandler.tagGet("logname")
        self.logdescription=self.taghandler.tagGet("logdescription")
        self.userErrormsg=self.taghandler.tagGet("userErrormsg")
        self.internalErrormsg=self.taghandler.tagGet("internalErrormsg")
        self.loglocation=self.taghandler.tagGet("loglocation")
        self.logtimestamp=self.taghandler.tagGet("logtimestamp")
        #self.params=self.taghandler.tagGet("params")


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

    __repr__ = __str__