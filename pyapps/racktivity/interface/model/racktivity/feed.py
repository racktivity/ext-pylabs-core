from enumerations import *
import pymodel as model


class feedConnector(model.Model):

    #@doc status of powerport
    status = model.Enumeration(feedConnectorStatusType,thrift_id=1)

    #@doc name of the feedconnector port
    name = model.String(thrift_id=2)

    #@doc sequence of feedconnector
    sequence = model.Integer(thrift_id=3)

    #@doc cable to which the feedconnector is connected
    cableguid = model.GUID(thrift_id=4)

# @doc physical feed
class feed(model.RootObjectModel):

    #@doc guid of the datacenter where the feed is located.
    datacenterguid = model.GUID(thrift_id=1)

    #@doc feed name
    name = model.String(thrift_id=2)

    #@doc additional remarks on feed
    description = model.String(thrift_id=3)

    #@doc connectors for devices linked to the feed
    feedconnectors = model.List(model.Object(feedConnector),thrift_id=4)

    #@doc feed type
    productiontype = model.Enumeration(feedProductionType,thrift_id=5)
    
    #@doc system
    system = model.Boolean(thrift_id=6)
    
    #@doc series of tags format
    tags = model.String(thrift_id=7)
    
    co2emission = model.Dict(model.Float(), thrift_id=8)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=9)