from enumerations import *
import pymodel as model


# @doc None
class resourcegroup(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description (optional)
    description = model.String(thrift_id=2)

    #@doc guid of the datacenter to which the resourcegroup belongs
    datacenterguid = model.GUID(thrift_id=3)

    #@doc group of devices part of this resourcegroup
    deviceguids = model.List(model.GUID(),thrift_id=4)

    #@doc group of backplanes part of this resourcegroup
    backplaneguids = model.List(model.GUID(),thrift_id=5)

    #@doc system
    system = model.Boolean(thrift_id=6)
    
    #@doc series of tags format
    tags = model.String(thrift_id=7)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=8)
