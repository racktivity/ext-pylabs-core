from enumerations import *
import pymodel as model

from acl import acl

# @doc None
class backplane(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description of the object
    description = model.String(thrift_id=2)

    #@doc type of backplane, storage, vlan host, management, and/or public
    backplanetype = model.Enumeration(backplanetype,thrift_id=3)

    #@doc flag indicating if backplane is ment to be connected to the outside world
    publicflag = model.Boolean(thrift_id=4)

    #@doc flag indicating if the backplane is hosting management Q-LAN's
    managementflag = model.Boolean(thrift_id=5)

    #@doc flag indicating if the backplane is used for storage purposes
    storageflag = model.Boolean(thrift_id=6)

    #@doc system
    system = model.Boolean(thrift_id=7)
    
    #@doc series of tags format
    tags = model.String(thrift_id=8)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),,thrift_id=9)
