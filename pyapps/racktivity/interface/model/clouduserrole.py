from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
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

    #@doc access control list
    acl = model.Object(acl,thrift_id=4)