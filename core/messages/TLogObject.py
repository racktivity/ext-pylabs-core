from pylabs import q
from MessageObject import MessageObject
import json

from pylabs import q
from MessageObject import MessageObject
from pylabs.Shell import *
from pylabs.baseclasses import BaseType
import json

import string



class TLogObject(MessageObject,BaseType):
    """
    implements http://pylabs.org/display/PM/RPC+Message
    """
    domain = q.basetype.string(doc="is a logical grouping and needs unique name e.g. an appname e.g. eereservationsystem",allow_none=False)
    category = q.basetype.string(doc="category in domain, e.g. customer",allow_none=False)    
    name = q.basetype.string(doc="is a logical name e.g. registration",allow_none=False)
    rootobjecttype = q.basetype.string(doc="if related to rootobject, specify type",allow_none=True)
    rootobjectguid = q.basetype.string(doc="if related to rootobject, guid of the ro",allow_none=True)
    jobguid = q.basetype.string(doc="if related to job, guid of the job",allow_none=True)
    params = q.basetype.dictionary(doc="parameters",allow_none=True)  #@todo does not work, why not?

    def __init__(self,messagestr=""):
        MessageObject.__init__(self,messagestr)
        self.mtype=q.enumerators.MessageType.TLOG
        self.type=q.enumerators.TlogType.OTHER
        self.rootobjecttype=""
        self.rootobjectguid=""
        self.jobguid=""
        if messagestr<>"":
            self._fromString(messagestr)
            self.tagBodyDecode()

    def init(self,type="",domain="",category="",name="",params={},rootobjecttype="",rootobjectguid="",tags="",jobguid=""):
        self.level=0
        self.jobguid=jobguid
        if not isinstance(params,dict):
            raise ValueError("Params need to be in dict format, like used in tasklets.")
        self.domain=domain
        self.params=params
        self.name=name
        self.category=category
        if type<>"":            
            self.type=type        
        if tags<>"":
            self.tags=tags
        self.rootobjecttype=rootobjecttype
        self.rootobjectguid=rootobjectguid        
        self.tagBodyEncode()            
        
    def getMessageString(self,multiline=False):
        self.tagBodyEncode()
        return MessageObject.getMessageString(self,multiline)
        
    def tagBodyEncode(self):
        """
        encode custom properties to body & tags of messageobject
        """
        self.body=json.dumps(self.params)
        self.taghandler.tagSet("domain", self.domain)
        if self.rootobjecttype<>"":
            self.taghandler.tagSet("rootobjecttype",self.rootobjecttype)
        if self.rootobjectguid<>"":
            self.taghandler.tagSet("rootobjectguid",self.rootobjectguid)
        self.taghandler.tagSet("category",self.category)
        if self.jobguid<>"":
            self.taghandler.tagSet("jobguid",self.jobguid)
        self.taghandler.tagSet("name",self.name)
        self.taghandler.tagSet("type",int(self.type))
        #self.body=self.body.strip()
        
        
    def tagBodyDecode(self,tagstring="",body=""):
        """
        decode body & tags to properties
        """
        if body<>"":
            self.body=body
        if tagstring<>"":
            self.tag=tagstring
        self.params=json.loads(self.body)
        self.domain=self.taghandler.tagGet("domain")
        self.category=self.taghandler.tagGet("category")
        self.name=self.taghandler.tagGet("name")
        self.type=q.enumerators.TlogType.getByLevel(int(self.taghandler.tagGet("type")))
        if self.taghandler.tagExists("jobguid"):
            self.jobguid=self.taghandler.tagGet("jobguid")
        if self.taghandler.tagExists("rootobjecttype"):
            self.jobguid=self.taghandler.tagGet("rootobjecttype")
        if self.taghandler.tagExists("rootobjectguid"):
            self.jobguid=self.taghandler.tagGet("rootobjectguid")
            
    def __str__(self):
        """
        nice formatting message        
        """
        self.tagBodyEncode()
        messagestr="type:%s agent:%s application:%s tags:%s\n%s" % (self.mtype,\
            self.agent,\
            self.application,\
            self._strEncode(self.tags),\
            self._strEncode(self.body)\
            )        
        return q.console.formatMessage(messagestr,prefix="log",withStar=True,indent=0)

    __repr__ = __str__
    
    def _strshort(self):
        """
        nice formatting message
        """
        self.tagBodyEncode()
        messagestr="%s" % (self.tags)
        return q.console.formatMessage(messagestr,prefix="",withStar=True,indent=0,width=120)
