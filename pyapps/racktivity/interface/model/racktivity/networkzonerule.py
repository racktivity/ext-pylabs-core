from enumerations import *
import pymodel as model

# @doc None
class ipzonerule(model.Model):

    #@doc None
    iprange = model.String(thrift_id=1)

    #@doc None
    portrange = model.String(thrift_id=2)

    #@doc None
    allow = model.Boolean(thrift_id=3)

    #@doc None
    log = model.String(thrift_id=4)

    #@doc None
    disabled = model.Boolean(thrift_id=5)

    #@doc None
    custom = model.String(thrift_id=6)



# @doc None
class networkzonerule(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description of the object
    description = model.String(thrift_id=2)

    #@doc None
    sourcenetworkzoneguid = model.GUID(thrift_id=3)

    #@doc None
    destnetworkzoneguid = model.GUID(thrift_id=4)

    #@doc None
    nrhops = model.Integer(thrift_id=5)

    #@doc None
    gatewayip = model.String(thrift_id=6)

    #@doc None
    log = model.String(thrift_id=7)

    #@doc None
    disabled = model.Boolean(thrift_id=8)

    #@doc None
    freetransit = model.Integer(thrift_id=9)

    #@doc None
    priority = model.Integer(thrift_id=10)

    #@doc None
    ipzonerules = model.List(model.Object(ipzonerule),thrift_id=11)

    #@doc system
    system = model.Boolean(thrift_id=12)
    
        #@doc series of tags format
    tags = model.String(thrift_id=13)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=14)