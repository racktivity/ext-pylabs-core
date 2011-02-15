from pylabs import q
from MessageObject import MessageObject
from pylabs.Shell import *
from pylabs.baseclasses import BaseType
import json

import string

class JobMessageObject(MessageObject,BaseType):
    """
    implements http://pylabs.org/display/PM/JobMessage
    """
    jobguid = q.basetype.string(doc="Unique job id",allow_none=False)
    name = q.basetype.string(doc="Job Name",allow_none=False)
    description = q.basetype.string(doc="Job Description",allow_none=True)
    userErrormsg = q.basetype.string(doc="enduser error message when job goes wrong",default="")
    internalErrormsg = q.basetype.string(doc="internal error message when job goes wrong",default="")
    maxduration = q.basetype.integer(doc="Job maxduration in seconds",allow_none=False,default=120)
    parentjobguid =q.basetype.string(doc="Job parentjobguid",default="")
    status = q.basetype.object(q.enumerators.JobStatusType,doc="Job Status",allow_none=False)
    starttime = q.basetype.integer(doc="Job starttime",default=0)
    endtime = q.basetype.integer(doc="Job endtime",default=0)
    params = q.basetype.dictionary(doc="parameters for the RPC call",allow_none=True) 
    domain = q.basetype.string(doc="when job is started as result of an action, domain (e.g. SmartStyleOffice) ")
    category = q.basetype.string(doc="when job is started as result of an action, category (e.g. machine)",allow_none=True) 
    methodname = q.basetype.string(doc="when job is started as result of an action,  methodname (e.g. start)",allow_none=True) 
    callerid = q.basetype.string(doc="when job is started as result of an action, Agent id of who asked for this action, e.g. when result of RPCMessage we know the caller",allow_none=True)

    def __init__(self,messagestr=""):
        """
        JobMessageObject:Create messagestring for the message type:Job
        """        
        MessageObject.__init__(self,messagestr)
        self.mtype = q.enumerators.MessageType.JOB    
        self.status=q.enumerators.JobStatusType.CREATED
        self.params={}
        if messagestr<>"":
            self._fromString(messagestr)
            self.tagBodyDecode()     
        
    def getActionName(self):
        """
        generate an actionname out of domain,category & methodname
        """
        return "%s__%s__%s" % (self.domain,self.category,self.methodname)
    
    def getMessageString(self):
        self.tagBodyEncode()
        return MessageObject.getMessageString(self)
        
    def tagBodyEncode(self):
        """
        encode custom properties to body & tags of JobMessageObject
        """
        self.body=json.dumps(self.params)
        self.taghandler.tagSet("jobguid",self.jobguid)
        self.taghandler.tagSet("name",self.name)
        self.taghandler.tagSet("description", self._strEncode(self.description))
        self.taghandler.tagSet("userErrormsg", self._strEncode(self.userErrormsg))
        self.taghandler.tagSet("internalErrormsg", self._strEncode(self.internalErrormsg))
        self.taghandler.tagSet("maxduration", self.maxduration)  
        self.taghandler.tagSet("parentjobguid", self.parentjobguid)
        self.taghandler.tagSet("status", self.status)
        self.taghandler.tagSet("starttime", self.starttime)
        self.taghandler.tagSet("endtime", self.endtime)
        self.taghandler.tagSet("params", self.params)
        self.taghandler.tagSet("domain", self.domain)
        self.taghandler.tagSet("category", self.category)
        self.taghandler.tagSet("methodname", self.methodname)
        
        
    def tagBodyDecode(self,tagstring="",body=""):
        """
        decode body & tags to properties
        """
        if body<>"":
            self.body=body
        self.params=json.loads(self.body)
        self.name=self.taghandler.tagGet("name")
        self.jobguid=self.taghandler.tagGet("jobguid")
        self.description=self._strDecode(self.taghandler.tagGet("description"))
        self.userErrormsg=self._strDecode(self.taghandler.tagGet("userErrormsg"))
        self.internalErrormsg= self._strDecode(self.taghandler.tagGet("internalErrormsg"))
        self.maxduration=self.taghandler.tagGet("maxduration")  
        self.parentjobguid=self.taghandler.tagGet("parentjobguid")
        self.status=self.taghandler.tagGet("status")
        self.starttime=self.taghandler.tagGet("starttime")
        self.endtime=self.taghandler.tagGet("endtime")
        self.params=self.taghandler.tagGet("params")
        self.domain=self.taghandler.tagGet("domain")
        self.category=self.taghandler.tagGet("category")
        self.methodname=self.taghandler.tagGet("methodname")


    def getMessageString(self,multiline=False):
        self.tagBodyEncode()
        return MessageObject.getMessageString(self,multiline)           

    