import pymodel as model
from acl import acl

# @doc
class autodiscoverysnmpmap(model.RootObjectModel):
    #@doc id of the manufacturer(ACP, avocent)
    manufacturer = model.String(thrift_id=1)
    #@doc model ID, the value u get when u call SNMP call for OID 1.3.6.1.2.1.1.2
    sysobjectid = model.String(thrift_id=2)
    #@doc oidmapping, maps a spefic data type to a oid
    oidmapping = model.Dict(model.String(), thrift_id=3)
    
    system = model.Boolean(thrift_id=4)
    
    tags = model.String(thrift_id=5)
    #@doc access control list
    acl = model.Object(acl,thrift_id=6)
