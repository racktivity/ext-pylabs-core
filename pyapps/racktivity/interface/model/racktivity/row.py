from enumerations import *
import pymodel as model
from acl import acl

# @doc row
class row(model.RootObjectModel):

    #@doc enterprise official name
    name = model.String(thrift_id=1)

    alias = model.String(thrift_id=2)

    #@doc Room where the row is located
    room = model.GUID(thrift_id=3)

    #@doc Pod where the row is located
    pod = model.GUID(thrift_id=4)

    #@doc List of racks in the row
    racks = model.List(model.GUID(), thrift_id=5)

    #@doc additional remarks on the row
    description = model.String(thrift_id=6)

    #@doc system 
    system = model.Boolean(thrift_id=7)

    #@doc series of tags format
    tags = model.String(thrift_id=8)

    #@doc access control list
    acl = model.Object(acl,thrift_id=9)