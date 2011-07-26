from enumerations import *
import pymodel as model


# @doc a space in the cloud, used to group cloudservices
class cloudspace(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description of the object
    description = model.String(thrift_id=2)

    #@doc status
    status = model.Enumeration(cloudspacestatustype,thrift_id=3)

    #@doc guid of cloudspace this cloudspace belongs to (optional, used to create a subspace)
    parentcloudspaceguid = model.GUID(thrift_id=4)

    #@doc guid of customer which owns this cloudspace
    customerguid = model.GUID(thrift_id=5)
    
    #@doc system
    system = model.Boolean(thrift_id=6)
    
    #@doc series of tags format
    tags = model.String(thrift_id=7)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=8)