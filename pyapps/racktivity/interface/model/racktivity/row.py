from enumerations import *
import pymodel as model


# @doc row
class row(model.RootObjectModel):

    #@doc enterprise official name
    name = model.String(thrift_id=1)

    alias = model.String(thrift_id=2)

    #@doc Room where the row is located
    roomguid = model.GUID(thrift_id=3)

    #@doc Pod where the row is located
    podguid = model.GUID(thrift_id=4)

    #@doc additional remarks on the row
    description = model.String(thrift_id=5)

    #@doc system 
    system = model.Boolean(thrift_id=6)

    #@doc series of tags format
    tags = model.String(thrift_id=7)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=9)