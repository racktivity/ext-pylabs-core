from enumerations import *
import pymodel as model
from acl import acl

# @doc a group of cloudusers
class cloudusergroup(model.RootObjectModel):

    #@doc name of clouduser
    name = model.String(thrift_id=1)

    #@doc optional description of clouduser
    description = model.String(thrift_id=2)

    #@doc cloudusers who belong to group
    cloudusers = model.List(model.GUID(),thrift_id=3)

    #@doc groups who belong to group
    cloudusergroups = model.List(model.GUID(),thrift_id=4)

    #@doc system
    system = model.Boolean(thrift_id=5)
    
    #@doc user roles belonging to the clouduser
    clouduserroles = model.List(model.GUID(),thrift_id=6)

    #@doc series of tags format
    tags = model.String(thrift_id=7)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=8)
