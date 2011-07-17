from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model

# @doc None
class networkzonerange(model.Model):

    #@doc None
    fromip = model.String(thrift_id=1)

    #@doc None
    toip = model.String(thrift_id=2)

from acl import acl

# @doc None
class networkzone(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description of the object
    description = model.String(thrift_id=2)

    #@doc is this network zone public to the internet ? Is informational of nature.
    public = model.Boolean(thrift_id=3)

    #@doc None
    datacenterguid = model.GUID(thrift_id=4)

    #@doc None
    parentnetworkzoneguid = model.GUID(thrift_id=5)

    #@doc None
    ranges = model.List(model.Object(networkzonerange),thrift_id=6)

    #@doc system
    system = model.Boolean(thrift_id=7)
    
    #@doc series of tags format
    tags = model.String(thrift_id=8)

    #@doc access control list
    acl = model.Object(acl,thrift_id=9)