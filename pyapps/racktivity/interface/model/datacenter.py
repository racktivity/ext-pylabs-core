from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
from acl import acl

class coordinates(model.Model):
    latitude = model.Float(thrift_id=1)
    longitude = model.Float(thrift_id=2)

# @doc physical datacenter
class datacenter(model.RootObjectModel):

    #@doc guid of the location of the datacenter
    locationguid = model.GUID(thrift_id=1)

    #@doc guid of the clouduser owning the datacenter
    clouduserguid = model.GUID(thrift_id=2)

    #@doc datacenter name
    name = model.String(thrift_id=3)

    #@doc additional remarks on datacenter
    description = model.String(thrift_id=4)
    
    #@doc system
    system = model.Boolean(thrift_id=5)
    
    #@doc series of tags format
    tags = model.String(thrift_id=6)
    
    coordinates = model.Object(coordinates, thrift_id=7)

    #@doc access control list
    acl = model.Object(acl,thrift_id=8)