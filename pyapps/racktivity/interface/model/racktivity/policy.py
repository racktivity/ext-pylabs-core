from enumerations import *
import pymodel as model


# @doc class which provides the properties of a policy
class policy(model.RootObjectModel):

    #@doc name of the policy
    name = model.String(thrift_id=1)

    #@doc description of the policy
    description = model.String(thrift_id=2)

    #@doc name of the rootobject type
    rootobjecttype = model.String(thrift_id=3)

    #@doc rootobject action name
    rootobjectaction = model.String(thrift_id=4)

    #@doc rootobject action name
    rootobjectguid = model.GUID(thrift_id=5)

    #@doc parameters to pass to the action. use Python dictionary format e.g. {"parameter1": "value1", "parameter2": "value2"}
    policyparams = model.String(thrift_id=6)

    #@doc interval in minutes.
    interval = model.Float(thrift_id=7)

    #@doc time ranges in which this action can only be executed. use Python list of tuples format e.g. [("00.00", "02.00"), ("04.00", "06.00")]
    runbetween = model.String(thrift_id=8)

    #@doc time ranges in which this action cannot be executed. use Python list of tuples format e.g. [("08.00", "12.00"), ("14.00", "18.00")]
    runnotbetween = model.String(thrift_id=9)

    #@doc last time the policy ran.
    lastrun = model.String(thrift_id=10)

    #@doc system
    system = model.Boolean(thrift_id=11)
    
    #@doc status
    status = model.Enumeration(policystatustype,thrift_id = 12)

    #@doc maxruns The number of concurrent runs
    maxruns = model.Integer(thrift_id=13)
    
    #@doc max duration in seconds
    maxduration = model.Integer(thrift_id=14)

    #@doc series of tags format
    tags = model.String(thrift_id=15)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=16)
