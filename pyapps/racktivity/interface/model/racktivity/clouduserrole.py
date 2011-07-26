from enumerations import *
import pymodel as model
from acl import acl

# @doc a group of cloudusers
class clouduserrole(model.RootObjectModel):

    #@doc name of clouduserrole
    name = model.String(thrift_id=1)

    #@doc optional description of clouduserrole
    description = model.String(thrift_id=2)
    
    #@doc series of tags format
    tags = model.String(thrift_id=3)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=4)