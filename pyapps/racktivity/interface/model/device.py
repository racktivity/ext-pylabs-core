from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
from acl import acl

# @doc physical disk  (nothing todo with the logical disk)
class pdisk(model.Model):

    #@doc string which defines location the device e.g. /dev/sda
    deviceid = model.String(thrift_id=1)

    #@doc disk size in GB e.g. 160
    size = model.Integer(thrift_id=2)

    #@doc disk rotations per minute e.g. 7200
    rpm = model.Integer(thrift_id=3)

    #@doc disk interface type
    diskinterfacetype = model.Enumeration(diskinterfacetype,thrift_id=4)

    #@doc disk status
    status = model.Enumeration(devicediskstatustype,thrift_id=5)


# @doc physical network interface in a device
class nicport(model.Model):

    #@doc hardware type of nicport
    nicporttype = model.Enumeration(nicporttype,thrift_id=1)

    #@doc status of nicport
    status = model.Enumeration(nicportstatustype,thrift_id=2)

    #@doc hardware address like macaddr
    hwaddr = model.String(thrift_id=3)

    #@doc backplane to which the nicport is connected
    backplaneguid = model.GUID(thrift_id=4)

    #@doc name of the nic port
    name = model.String(thrift_id=5)

    #@doc sequence of nic port
    sequence = model.String(thrift_id=6)

    #@doc cable to which the nicport is connected
    cableguid = model.GUID(thrift_id=7)


# @doc device account e.g. BIOS account, firmware account
class account(model.Model):

    #@doc device account type
    deviceaccounttype = model.Enumeration(deviceaccounttype,thrift_id=1)

    #@doc device account login
    login = model.String(thrift_id=2)

    #@doc device account password
    password = model.String(thrift_id=3)


# @doc a device consists of components
class component(model.Model):

    #@doc component brand
    brand = model.String(thrift_id=1)

    #@doc component type
    componenttype = model.Enumeration(componenttype,thrift_id=2)

    #@doc component model identification
    modelnr = model.String(thrift_id=3)

    #@doc component serial number
    serialnr = model.String(thrift_id=4)

    #@doc batch number, can be used to identify components belonging to a bad vendor batch
    batchnr = model.String(thrift_id=5)

    #@doc firmware version
    firmware = model.String(thrift_id=6)

    #@doc label
    label = model.String(thrift_id=7)


# @doc physical network interface in a device
class powerport(model.Model):

    #@doc status of powerport
    status = model.Enumeration(powerportstatustype,thrift_id=1)

    #@doc name of the power port
    name = model.String(thrift_id=2)

    #@doc sequence of powerport
    sequence = model.String(thrift_id=3)

    #@doc cable to which the powerport is connected
    cableguid = model.GUID(thrift_id=4)

from acl import acl
class device(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc is template, when template used as example for an application
    template = model.Boolean(thrift_id=2)

    #@doc device type
    devicetype = model.Enumeration(devicetype,thrift_id=3)

    #@doc guid of the rack to which the device belongs - can be None e.g. for devices in stock or in repair
    rackguid = model.GUID(thrift_id=4)

    #@doc guid of the datacenter to which the device belongs - can be None e.g. for devices in stock or in repair
    datacenterguid = model.GUID(thrift_id=5)

    #@doc size of the device, measured in u e.g. 1u high
    racku = model.Integer(thrift_id=6)

    #@doc physical position of the device in a rack (y coordinate) measured in u slots
    racky = model.Integer(thrift_id=7)

    #@doc physical position of the device in the rack (z coordinate, 0 = front, 1 = back)
    rackz = model.Integer(thrift_id=8)

    #@doc model number of the device
    modelnr = model.String(thrift_id=9)

    #@doc serial number of the device
    serialnr = model.String(thrift_id=10)

    #@doc firmware identifier of the device
    firmware = model.String(thrift_id=11)

    #@doc remarks on the device
    description = model.String(thrift_id=12)

    #@doc last time device was inspected
    lastcheck = model.DateTime(thrift_id=13)

    #@doc device status
    status = model.Enumeration(devicestatustype,thrift_id=14)

    #@doc parent device, e.g. blade belongs to bladechasis
    parentdeviceguid = model.GUID(thrift_id=15)

    #@doc list of components which are part of the device , do not use fo disks & nics
    components = model.List(model.Object(component),thrift_id=16)

    #@doc physical disks which are part of device
    pdisks = model.List(model.Object(pdisk),thrift_id=17)

    #@doc nicports which are part of device
    nicports = model.List(model.Object(nicport),thrift_id=18)

    #@doc powerports which are part of device
    powerports = model.List(model.Object(powerport),thrift_id=19)

    #@doc date and time of last check on the device with reality
    lastrealitycheck = model.DateTime(thrift_id=20)

    #@doc list of accounts available in this device (e.g. bios accounts)
    accounts = model.List(model.Object(account),thrift_id=23)

    #@doc guid of the space to which this machine belongs
    cloudspaceguid = model.GUID(thrift_id=24)

    #@doc system
    system = model.Boolean(thrift_id=25)

    #@doc series of tags format
    tags = model.String(thrift_id=26)

    #@doc access control list
    acl = model.Object(acl,thrift_id=27)
