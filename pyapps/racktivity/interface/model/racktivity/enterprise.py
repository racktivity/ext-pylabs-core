from enumerations import *
import pymodel as model


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

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=6)