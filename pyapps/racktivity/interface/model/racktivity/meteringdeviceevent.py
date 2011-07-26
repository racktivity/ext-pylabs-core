from enumerations import *
import pymodel as model
from acl import acl

# @doc details of an meteringdeviceevent  occured on meteringdevice
class meteringdeviceevent(model.RootObjectModel):

        #@doc field for custom made event types, e.g 
        eventtype = model.String(thrift_id=1)
        
        #@doc epoch timestamp
        timestamp = model.Integer(thrift_id=2)

        #@doc int representing urgency or level of message e.g. in case of log message is loglevel
        level = model.Enumeration(meteringdeviceeventlevel,thrift_id=3)

        #@doc guid of the meteringdevice which generated the message
        meteringdeviceguid = model.GUID(thrift_id=4)

        #@doc port number if event has occured on port
        portsequence = model.Integer(thrift_id=5)
        
        #@doc sensor number if event has occured on sensor
        sensorsequence =  model.Integer(thrift_id=6)
        
        #@doc threshold guid, threshold linked to the event
        thresholdguid = model.GUID(thrift_id=7)
        
        #@doc series of tags format
        tags = model.String(thrift_id=8)

        #@doc public error message
        errormessagepublic = model.String(thrift_id=9)

        #@doc private error message
        errormessageprivate = model.String(thrift_id=10)

        #@doc logs of errorcondition
        logs = model.String(thrift_id=11)

        # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
        cloudusergroupactions = model.Dict(model.String(),thrift_id=22)