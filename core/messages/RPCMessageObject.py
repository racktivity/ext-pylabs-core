from pylabs import q
from MessageObject import MessageObject
from pylabs.Shell import *
from pylabs.baseclasses import BaseType
import json

import string

class RPCMessageObject(MessageObject,BaseType):
    """
    implements http://pylabs.org/display/PM/RPC+Message
    """
    domain = q.basetype.string(doc="rpc call needs to exist in a domain, is a logical grouping and needs unique name",allow_none=False)
    login = q.basetype.string(doc="login for rpccall to server/robbot",allow_none=True)
    passwd = q.basetype.string(doc="passwd for rpccall to server/robbot",allow_none=True)
    category = q.basetype.string(doc="category in which method call belongs e.g. machine",allow_none=False)    
    methodname = q.basetype.string(doc="method call name e.g. start",allow_none=False)
    params = q.basetype.dictionary(doc="parameters for the RPC call",allow_none=True)  #@todo does not work, why not?

    def __init__(self,messagestr=""):
        MessageObject.__init__(self,messagestr)
        self.mtype=q.enumerators.MessageType.RPC
        self.params={}
        if messagestr<>"":
            self._fromString(messagestr)
            self.tagBodyDecode()
        
    def init(self, domain, category, methodname, params={},login="",passwd="",tags=""):
        """
        
        @param tags can be usefull in advanced messaging/queuing scenario's (normally not used)
        """
        if tags<>"":
            self.tags = tags
        self.domain=domain
        self.category=category
        self.methodname=methodname
        self.params=params
        self.login=login
        self.passwd=passwd                    
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
        self.taghandler.tagSet("category", self.category)
        self.taghandler.tagSet("methodname", self.methodname)
        self.taghandler.tagSet("login", self.login)        
        self.taghandler.tagSet("passwd", self.passwd)
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
        self.methodname=self.taghandler.tagGet("methodname")
        if self.taghandler.tagExists("login"):
            self.login=self.taghandler.tagGet("login")
        if self.taghandler.tagExists("passwd"):
            self.passwd=self.taghandler.tagGet("passwd")

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
    