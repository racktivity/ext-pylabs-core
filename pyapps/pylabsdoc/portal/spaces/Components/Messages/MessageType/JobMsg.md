[basemsg]: /PyLabsdoc/#/Components/BaseMsg

## jobmessage

### basic [basemessage][basemsg] properties

* messagetype = q.enumerators.MessageType.JOB
* time (epoch = int)
* level : 0 (not used)
* agent : unique agent id (e.g. kdscp@mydomain.com) represents where job is created
* returnqueue : (only populated when using queues)
* source : application name where message was sent
* tags : holds additional JobMessage properties + extra optional tags & labels
* body : encoded string holding the params (json encoded)


### additional JobMessage properties

encoded as tags
* jobguid: as tag
* name : meaning full name of jon
* description : optional description of job
* userErrormsg : enduser error message when job goes wrong
* internalErrormsg : internal error message when job goes wrong
* maxduration :  Job maxduration in seconds
* parentjobguid : jobguid of parent
* status : status of job
* starttime : epoch int
* endtime : epoch int
* callerid : when job is started as result of an action, Agent id of who asked for this action, e.g. when result of RPCMessage we know the caller
* domain : when job is started as result of an action, domain (e.g. SmartStyleOffice)
* category : when job is started as result of an action, category (e.g. machine)
* methodname : when job is started as result of an action,  methodname (e.g. start)

encoded in body:
* params : in messagebody is json representation of dict of params (params dict like used in tasklets)


### Optional tags used

e.g.
* application (guid)
* vmachine (guid)
* pmachine (guid)


### jobstatustype

    q.enumerators.JobStatusType.CREATED     
    q.enumerators.JobStatusType.WAITING   
    q.enumerators.JobStatusType.DONE        
    q.enumerators.JobStatusType.UNKNOWN   
    q.enumerators.JobStatusType.ERROR      
    q.enumerators.JobStatusType.RUNNING     


### code examples


    message=q.messagehandler.getJobMessageObject()
    #we do it the long way there is also a rpccall.init(,,, method
    
    message.jobguid="3434-asdasdasd-asdasd"
    message.name="startmachine"
    message.description="will start machine"
    message.userErrormsg="Could not start vmachine with guid %s." % "sss-sdsdsdsdsdsd-ddd"
    
    message.starttime=q.base.time.getTimeEpoch()
    message.maxduration=120 
    
    message.domain="sso"
    message.category="machine"
    message.methodname="start"
    message.params["machineguid"]="aavbb-dfdsfsdfsd-dfff"
    
    message.callerid=q.application.agentid #is only correct if we are the originator of the call to the action which started this job
    
    print message.getMessageString()


#### example string representation of logmessage

* is result of : message.getMessageString(multiline=True)  #if printed without multiline True everything will be serialized on 1 line

    4|1266766167|0|unknown.somewhere.com||qshell|status:created category:machine domain:sso endtime:0 methodname:start description:will start machine inte
    rnalErrormsg: params:{'machineguid': 'aavbb-dfdsfsdfsd-dfff'} jobguid:3434-asdasdasd-asdasd starttime:1266766167 userErrormsg:Could not start vmachine
     with guid sss-sdsdsdsdsdsd-ddd. parentjobguid: maxduration:120 name:startmachine|
    {"machineguid": "aavbb-dfdsfsdfsd-dfff"}


### PyLabs

Inherits from the base MessageObject

[[code]]
class JobMessageObject(MessageObject,BaseType):
    """
    implements http://pylabs.org/display/PM/JobMessage
    """
    jobguid = q.basetype.string(doc="Unique job id",allow_none=False)
    name = q.basetype.string(doc="Job Name",allow_none=False)
    description = q.basetype.string(doc="Job Description",allow_none=True)
    userErrormsg = q.basetype.string(doc="Job userError Message",default="")
    internalErrormsg = q.basetype.string(doc="Job Internal Error Message",default="")
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
[[/code]]
