@metadata title=PyModel Message
@metadata tagstring=pymodel message model

[basemsg]: #/Components/BaseMsg


# PyModel Message

* send a changed pymodel message to a robot which will deal with the pymodel object and e.g. store it in a database or forward to another system or execute business logic


## basic [basemessage][basemsg] properties

* messagetype = q.enumerators.MessageType.PYMODEL
* time (epoch = int)
* level : 0 (not used)
* agent : unique agent id (e.g. kdscp@mydomain.com)
* returnqueue : (only populated when using queues)
* source : application name where message was sent
* tags : holds additional PymodelMessage properties + extra optional tags & labels
* body : thrift representation of pymodel


## additional PymodelMessage properties

* login (optional): as tag
* passwd (optional) : as tag
* domain (each pymodel object lives in a domain with a specific unique name) : as tag
* category (e.g. machine) : as tag
* state : new/delete/modified as tag
* model :in messagebody is json representation of dict of params (params dict like used in tasklets)


## Optional tags used

e.g.
* application (guid)
* vmachine (guid)
* pmachine (guid)
* job (guid or unique id) e.g. when e.g. this pymodel update message is happening in context of job


    machineModelObject=q.pymodel.core.machine.getEmptyModelObject()
    machineModelObject.name=...
    ... #fill in model
    
    message=q.messagehandler.getPymodelMessageObject()
    #we do it the long way there is also a rpccall.init(,,, method
    message.domain="sso"
    message.category="machine"
    message.state="new"
    message.model=machineModelObject
    message.login="qbase"
    message.passwd="nothing"                    
    print message.getMessageString()


## example string representation of logmessage

* is result of : message.getMessageString(multiline=True)  #if printed without multiline True everything will be serialized on 1 line


## PyLabs

Inherits from the base MessageObject

[[code]]
class PymodelMessageObject(MessageObject,BaseType):
   @todo

[[/code]]
