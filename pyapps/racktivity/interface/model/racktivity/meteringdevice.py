import pymodel as model
from enumerations import *

 # @doc account for managing access to the device       
class account(model.Model):

    #@doc login of the account to access the meteringdevice
    login = model.String(thrift_id=2)

    #@doc password of the account to access the meteringdevice
    password = model.String(thrift_id=3)


# @doc class which provides the properties of a meteringdevice  port
class port(model.Model):

    #@doc label of the input
    label = model.String(thrift_id=1)

    #@doc sequence of the port
    sequence = model.Integer(thrift_id=2)
    
    #@doc porttype, listed in the enumerator PortType
    porttype = model.Enumeration(porttype,thrift_id=3)
    
    #@doc specific attributes for this port
    attributes = model.Dict(model.String(), thrift_id=4)
    

# @doc class which provides the properties of a metering device sensor
class sensor(model.Model):

    #@doc label of the sensor
    label = model.String(thrift_id=1)

    #@doc sequence of the sensor
    sequence = model.Integer(thrift_id=2)
    
    #@doc sensor type, listed in the enumerator SensorType
    sensortype = model.Enumeration(sensortype,thrift_id=3)
    
     #@doc guid of the thresholds which are defined on the sensor
    thresholdguids = model.List(model.GUID(),thrift_id=4)
    
    #@doc specific attributes for this sensor
    attributes = model.Dict(model.String(), thrift_id=5)

# @doc class which provides the properties of a metering device input
class powerports(model.Model):

    #@doc label of the input
    label = model.String(thrift_id=1)

    #@doc sequence of the port
    sequence = model.Integer(thrift_id=2)
    
    #@doc guid of the cable to which the power input is connected
    cableguid = model.GUID(thrift_id=3)
    
    #@doc specific attributes for this powerinput
    attributes = model.Dict(model.String(), thrift_id=4)

class network(model.Model):
    #@doc hardware address like macaddr
    ipaddress = model.String(thrift_id=1)
    port = model.Integer(thrift_id=2)
    protocol = model.String(thrift_id=3)

from acl import acl
# @doc power device
class meteringdevice(model.RootObjectModel):
    
    #@doc name of the object
    name = model.String(thrift_id=1)
    
    #@doc id of the the slave e.g T1, P1
    id = model.String(thrift_id=2)
    
    #@doc meteringdevicetype, string that specify the type of meteringdevice
    meteringdevicetype = model.String(thrift_id=3)

    #@doc guid of the parent meteringdevice, in case of master/slave configurations
    parentmeteringdeviceguid = model.GUID(thrift_id=4)
   
    #@doc rack of datacenter in which the meteringdevice is located
    rackguid = model.GUID(thrift_id=5)

    #@doc guid of the clouduser owning the meteringdevice
    clouduserguid = model.GUID(thrift_id=6)

    #@doc X position of the meteringdevice in the rack, a sequence from left to right (0=most left, 1=one next to that, ..., 10=most right)
    positionx = model.Integer(thrift_id=7)

    #@doc Y position of the meteringdevice in the rack, expressed in U
    positiony = model.Integer(thrift_id=8)

    #@doc Z position of the meteringdevice in the rack (0=front, 1=back)
    positionz = model.Integer(thrift_id=9)

    #@doc asset height in U
    height = model.Integer(thrift_id=10)

    #@doc list of power inputs for the meteringdevice
    powerinputs = model.List(model.Object(powerports),thrift_id=11)
    
    #@doc list of power outputs for the meteringdevice
    poweroutputs = model.List(model.Object(powerports),thrift_id=12)
    
    #@doc list of sensors for the meteringdevice
    sensors = model.List(model.Object(sensor),thrift_id=13)
 
    #@doc guid of the application which holds all SNMP related information
    snmpapplicationguid = model.String(thrift_id=15)
    
    #@doc list of ports(e.g serial, ...) connected to the device
    ports = model.List(model.Object(port),thrift_id=16)
    
    #@doc list of accounts who can access the meteringdevice
    accounts = model.List(model.Object(account),thrift_id=17)
    
    #@doc is template, when template used as template for the meteringdevice
    template = model.Boolean(thrift_id=18)
    
    #@doc series of tags format
    tags = model.String(thrift_id=19)
    
    #@doc meteringdeviceconfigstatus, listed in the enumerator meteringdeviceconfigstatus
    meteringdeviceconfigstatus = model.Enumeration(meteringdeviceconfigstatus,thrift_id=20)

    #@doc access control list
    acl = model.Object(acl,thrift_id=21)
    
    #@doc last accessed time
    lastaccessed = model.Integer(thrift_id=22)
    
    #@doc network information
    network = model.Object(network,thrift_id=23)
