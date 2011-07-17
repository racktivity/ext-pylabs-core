from enumerations import *
import pymodel as model

class dns(model.Model):

    #@doc ip of the dns server
    ip = model.String(thrift_id=1)

    #@doc order of the dns server
    order = model.Integer(thrift_id=2)

from acl import acl

# @doc None
class lan(model.RootObjectModel):

    #@doc name of the object
    name = model.String(thrift_id=1)

    #@doc additional remarks / description
    description = model.String(thrift_id=2)

    #@doc VLAN tag of this VLAN. VLAN tag 0 means that no VLAN technology is used.
    vlantag = model.Integer(thrift_id=3)

    #@doc guid of the backplane on which the LAN lives
    backplaneguid = model.GUID(thrift_id=4)

    #@doc flag indicating if the Q-LAN has a public IP addresses or not
    publicflag = model.Boolean(thrift_id=5)

    #@doc flag indicating if the Q-LAN is a management Q-LAN or not
    managementflag = model.Boolean(thrift_id=6)

    #@doc flag indicating if the Q-LAN is used for storage purposes
    storageflag = model.Boolean(thrift_id=7)

    #@doc flag indicating if the Q-LAN  will be used for DHCP purposes, all IP addresses in this range will be given out to machines which request an ipaddress & are not known to dhcpserver
    dhcpflag = model.Boolean(thrift_id=8)

    #@doc subnet of the Q-LAN, e.g. 192.168.0.0
    network = model.String(thrift_id=9)

    #@doc (optional) netmask of the Q-LAN subnet, e.g. 255.255.0.0
    netmask = model.String(thrift_id=10)

    #@doc default gateway of the Q-LAN, e.g. 192.168.0.1
    gateway = model.String(thrift_id=11)

    #@doc dns of the Q-LAN, e.g. 192.168.0.1
    dns = model.List(model.Object(dns),thrift_id=12)

    startip = model.String(thrift_id=13)

    #@doc end IP address, to define the IP range of the Q-LAN
    endip = model.String(thrift_id=14)

    #@doc guid of the parent lan (if any)
    parentlanguid = model.GUID(thrift_id=15)

    #@doc guid of the space to which this machine belongs
    cloudspaceguid = model.GUID(thrift_id=16)

    #@doc status of the lan
    status = model.Enumeration(lanstatustype,thrift_id=17)

    #@doc type of the lan
    lantype = model.Enumeration(lantype,thrift_id=18)

    #@doc macrange of the lan
    macrange = model.String(thrift_id=19)

    #@doc system
    system = model.Boolean(thrift_id=20)
    
    #@doc internetpublicflag
    internetpublicflag = model.Boolean(thrift_id=21)
    
    #@doc integratedflag 
    integratedflag = model.Boolean(thrift_id=22)
    
    #@doc series of tags format
    tags = model.String(thrift_id=23)

    #@doc access control list
    acl = model.Object(acl,thrift_id=24)