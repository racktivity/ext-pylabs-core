from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model

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
class powerinput(model.Model):

    #@doc label of the input
    label = model.String(thrift_id=1)

    #@doc sequence of the port
    sequence = model.Integer(thrift_id=2)
    
    #@doc guid of the cable to which the power input is connected
    cableguid = model.GUID(thrift_id=3)
    
    #@doc specific attributes for this powerinput
    attributes = model.Dict(model.String(), thrift_id=4)

# @doc class which provides the properties of a metering device output
class poweroutput(model.Model):

    #@doc label of the input
    label = model.String(thrift_id=1)

    #@doc sequence of the port
    sequence = model.Integer(thrift_id=2)
    
    #@doc guid of the cable to which the power input is connected
    cableguid = model.GUID(thrift_id=3)
    
    #@doc guid of the thresholds which are defined on the poweroutput
    thresholdguids = model.List(model.GUID(),thrift_id=4)

    #@doc specific attributes for this powerinput
    attributes = model.Dict(model.String(), thrift_id=5)
    
# @doc nic interface
class nic(model.Model):

    #@doc hardware address like macaddr
    hwaddr = model.String(thrift_id=1)

    #@doc type of nic
    nictype = model.Enumeration(nictype,thrift_id=2)

    #@doc status of nic
    status = model.Enumeration(nicstatustype,thrift_id=3)

    #@doc NIC order to identify how the NICs come up e.g. 0 for eth0, 1 for eth1
    order = model.Integer(thrift_id=4)

    #@doc list of IP addresses on the NIC
    ipaddressguids = model.List(model.GUID(),thrift_id=5)    

from acl import acl
# @doc power device
class meteringdevice(model.RootObjectModel):
    
    #@doc name of the object
    name = model.String(thrift_id=1)
    
    #@doc id of the the slave e.g T1, P1
    id = model.String(thrift_id=2)
    
    #@doc meteringdevicetype, listed in the enumerator meteringdeviceype
    meteringdevicetype = model.Enumeration(meteringdevicetype,thrift_id=3)

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
    powerinputs = model.List(model.Object(powerinput),thrift_id=11)
    
    #@doc list of power outputs for the meteringdevice
    poweroutputs = model.List(model.Object(poweroutput),thrift_id=12)
    
    #@doc list of sensors for the meteringdevice
    sensors = model.List(model.Object(sensor),thrift_id=13)
     
    #@doc list of NICs on the machine
    nics = model.List(model.Object(nic),thrift_id=14)
 
    #@doc guid of the application which holds all SNMP related information
    snmpapplicationguid = model.String(thrift_id=15)

    #@doc specific attributes e.g oled brighteness.
    attributes = model.Dict(model.String(), thrift_id=16)
    
    #@doc list of ports(e.g serial, ...) connected to the device
    ports = model.List(model.Object(port),thrift_id=17)
    
    #@doc list of accounts who can access the meteringdevice
    accounts = model.List(model.Object(account),thrift_id=18)
    
    #@doc is template, when template used as template for the meteringdevice
    template = model.Boolean(thrift_id=19)
    
    #@doc series of tags format
    tags = model.String(thrift_id=20)
    
    #@doc meteringdeviceconfigstatus, listed in the enumerator meteringdeviceconfigstatus
    meteringdeviceconfigstatus = model.Enumeration(meteringdeviceconfigstatus,thrift_id=21)
    
    #@doc meteringdeviceconfigstatus, listed in the enumerator meteringdeviceconfigstatus
    collectorguid = model.GUID(thrift_id=22)

    #@doc access control list
    acl = model.Object(acl,thrift_id=23)
    
    #@doc last accessed time
    lastaccessed = model.Integer(thrift_id=24)

