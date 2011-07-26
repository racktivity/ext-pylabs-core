from enumerations import *
import pymodel as model

class coordinates(model.Model):
    latitude = model.Float(thrift_id=1)
    longitude = model.Float(thrift_id=2)

from acl import acl

# @doc class which provides the properties of a location of a data center
class location(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description of the object
    description = model.String(thrift_id=2)

    #@doc alias for a location
    alias = model.String(thrift_id=3)

    #@doc indicator if location is a public location or not
    public = model.Boolean(thrift_id=4)

    #@doc address of the location of a data center
    address = model.String(thrift_id=5)

    #@doc city where the data center is located
    city = model.String(thrift_id=6)

    #@doc country where the data center is located
    country = model.String(thrift_id=7)

    #@doc country where the data center is located
    timezonename = model.String(thrift_id=8)

    #@doc country where the data center is located
    timezonedelta = model.String(thrift_id=9)
    
    #@doc system
    system = model.Boolean(thrift_id=10)

    #@doc series of tags format
    tags = model.String(thrift_id=11)
    
    coordinates = model.Object(coordinates, thrift_id=12)

    # A dictionary in the form {'group1_action1':None, 'group2_action1':None, 'group1_action2': None}
    cloudusergroupactions = model.Dict(model.String(),thrift_id=13)