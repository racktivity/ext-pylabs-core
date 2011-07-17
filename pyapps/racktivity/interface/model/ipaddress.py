from pylabs.baseclasses.BaseEnumeration import BaseEnumeration
import pymodel as model
from acl import acl

# @doc None
class ipaddress(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc description of the object
    description = model.String(thrift_id=2)

    #@doc IP address of the IP
    address = model.String(thrift_id=3)

    #@doc netmask of the IP object
    netmask = model.String(thrift_id=4)

    #@doc flag indicating if the IP is blocked
    block = model.Boolean(thrift_id=5)

    #@doc type of the IP object, STATIC or DHCP
    iptype = model.Enumeration(iptype,thrift_id=6)

    #@doc version of the IP object, IPV4 or IPV6
    ipversion = model.Enumeration(ipversion,thrift_id=7)

    #@doc lan to which the ip is connected
    languid = model.GUID(thrift_id=8)

    #@doc status of the ip
    status = model.Enumeration(ipstatustype,thrift_id=9)

    #@doc flags whether ipaddress is virtual or not
    virtual = model.Boolean(thrift_id=10)
    
    #@doc system
    system = model.Boolean(thrift_id=11)
    
    #@doc series of tags format
    tags = model.String(thrift_id=12)

    #@doc access control list
    acl = model.Object(acl,thrift_id=13)