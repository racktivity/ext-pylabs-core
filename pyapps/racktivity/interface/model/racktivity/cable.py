from enumerations import *
import pymodel as model


# @doc physical cable connecting two device ports
class cable(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description of the object
    description = model.String(thrift_id=2)

    #@doc cable type
    cabletype = model.Enumeration(cabletype,thrift_id=3)

    #@doc label attached to cable
    label = model.String(thrift_id=4)
    
    #@doc system
    system = model.Boolean(thrift_id=5)

    #@doc series of tags format
    tags = model.String(thrift_id=6)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=7)