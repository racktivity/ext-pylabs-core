from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
from acl import acl

# @doc enterprise
class enterprise(model.RootObjectModel):

    #@doc guid of the enterprise headquarters location
    campuses  = model.List(model.GUID(),thrift_id=1)
    
    #@doc enterprise official name
    name = model.String(thrift_id=2)

    #@doc additional remarks on the enterprise
    description = model.String(thrift_id=3)
    
    #@doc system
    system = model.Boolean(thrift_id=4)
    
    #@doc series of tags format
    tags = model.String(thrift_id=5)

    #@doc access control list
    acl = model.Object(acl,thrift_id=6)