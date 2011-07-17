from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
from acl import acl

# @doc rack in the datacenter
class rack(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description of the object
    description = model.String(thrift_id=2)

    #@doc datacenter to which the rack belongs
    datacenterguid = model.GUID(thrift_id=3)

    #@doc floor location of the rack in the datacenter
    floor = model.String(thrift_id=4)

    #@doc corridor location of the rack on the floor
    corridor = model.String(thrift_id=5)

    #@doc position of the rack in the corridor or datacenter
    position = model.String(thrift_id=6)

    #@doc rack height in u
    height = model.Integer(thrift_id=7)

    #@doc racktype, listed in the enumerator racktype
    racktype = model.Enumeration(racktype,thrift_id=8)

    #@doc system
    system = model.Boolean(thrift_id=9)

    #@doc series of tags format
    tags = model.String(thrift_id=10)
    
    #@doc room to which the rack belongs
    roomguid = model.GUID(thrift_id=11)

    #@doc access control list
    acl = model.Object(acl,thrift_id=12)