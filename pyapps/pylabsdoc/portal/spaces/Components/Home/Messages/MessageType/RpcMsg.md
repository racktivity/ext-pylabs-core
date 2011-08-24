@metadata title=RPC Message
@metadata tagstring=rpc message

[basemsg]: #/Components/BaseMsg

# RPC Message


## basic [basemessage][basemsg] properties

* messagetype = q.enumerators.MessageType.RPC
* time (epoch = int)
* level : 0 (not used)
* agent : unique agent id (e.g. kdscp@mydomain.com)
* returnqueue : (only populated when using queues)
* source : application name where message was sent
* tags : holds additional RPCMessage properties + extra optional tags & labels
* body : encoded string holding additional RCP properties


## additional RPCMessage properties

* login (optional): as tag
* passwd (optional) : as tag
* domain (e.g. SmartStyleOffice) : as tag
* category (e.g. machine) : as tag
* methodname (e.g. start) : as tag
* params :in messagebody is json representation of dict of params (params dict like used in tasklets)


## Optional tags used

e.g.
* application (guid)
* vmachine (guid)
* pmachine (guid)
* job (guid or unique id) e.g. when RPC call was linked to a job


## code examples

    rpccall=q.messagehandler.getRPCMessageObject()
    #we do it the long way there is also a rpccall.init(,,, method
    rpccall.domain="sso"
    rpccall.category="machine"
    rpccall.methodname="start"
    rpccall.params["machineguid"]="aavbb-dfdsfsdfsd-dfff"
    rpccall.login="qbase"
    rpccall.passwd="nothing"                    
    #rpccall.tagBodyEncode()  ##can call this optionally but is not needed if later getRPCMessage or a messagehandler send method is used
    print rpccall.getMessageString()


## example string representation of logmessage

* is result of : message.getMessageString(multiline=True)  #if printed without multiline True everything will be serialized on 1 line

    0|1266761366|0|unknown.somewhere.com||qshell|category:machine passwd:nothing domain:sso methodname:start login:qbase|
    {"machineguid": "aavbb-dfdsfsdfsd-dfff"}


## PyLabs

Inherits from the base MessageObject

[[code]]
class RPCMessageObject(MessageObject,BaseType):
    """
    implements http://PyLabs.org/display/PM/RPC+Message
    """
    domain = q.basetype.string(doc="rpc call needs to exist in a domain, is a logical grouping and needs unique name",allow_none=False)
    login = q.basetype.string(doc="login for rpccall to server/robbot",allow_none=True)
    passwd = q.basetype.string(doc="passwd for rpccall to server/robbot",allow_none=True)
    category = q.basetype.string(doc="category in which method call belongs e.g. machine",allow_none=False)    
    methodname = q.basetype.string(doc="method call name e.g. start",allow_none=False)
    params = q.basetype.dictionary(doc="parameters for the RPC call",allow_none=True)  #@todo does not work, why not?
[[/code]]
