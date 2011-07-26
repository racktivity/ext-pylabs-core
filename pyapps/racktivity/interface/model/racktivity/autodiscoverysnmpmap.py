import pymodel as model


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
    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=6)
