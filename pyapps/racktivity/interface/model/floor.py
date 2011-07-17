from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model

from acl import acl

# @doc pod
class floor(model.RootObjectModel):
    
    #@doc floor offical name
    name = model.String(thrift_id=1)
    
    #@doc Floor alias
    alias = model.String(thrift_id=2)

    #@doc Datacenter where the floor is located
    datacenterguid = model.GUID(thrift_id=3)
    
    #@doc The floor number
    floor = model.Integer(thrift_id=4)
    
    #@doc additional remarks on the floor
    description = model.String(thrift_id=6)
    
    #@doc system 
    system = model.Boolean(thrift_id=7)
    
    #@doc series of tags format
    tags = model.String(thrift_id=8)

    #@doc access control list
    acl = model.Object(acl,thrift_id=9)