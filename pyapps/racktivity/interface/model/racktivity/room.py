from enumerations import *
import pymodel as model
from acl import acl

# @doc room in the datacenter
class room(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description of the object
    description = model.String(thrift_id=2)

    #@doc datacenter to which the room belongs
    datacenterguid = model.GUID(thrift_id=3)

    #@doc floor location of the rack in the datacenter
    floor = model.String(thrift_id=4)

    #@doc alias for the room
    alias = model.String(thrift_id=5)

     #@doc system
    system = model.Boolean(thrift_id=6)

    #@doc series of tags format
    tags = model.String(thrift_id=7)


    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=8)
