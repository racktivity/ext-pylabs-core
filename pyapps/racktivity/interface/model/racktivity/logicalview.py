from enumerations import *
import pymodel as model


# @doc logical view
class logicalview(model.RootObjectModel):
    
    #@doc enterprise offical name
    name = model.String(thrift_id=1)

    #@doc definition of the view
    viewstring = model.String(thrift_id=2)

    #@doc description
    description = model.String(thrift_id=3)

    #@doc clouduser to which this logical view is linked
    clouduserguid = model.GUID(thrift_id=4)

    #@doc share, if true, the view is shared to all uses
    share = model.Boolean(thrift_id=5)

    #@doc system 
    system = model.Boolean(thrift_id=6)
    
    #@doc series of tags format
    tags = model.String(thrift_id=7)

   #@doc access control list
    cloudusergroupactions = model.Dict(model.String(),thrift_id=8)