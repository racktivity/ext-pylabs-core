@metadata title=CMDB SubObject
@metadata order=40
@metadata tagstring=cmdb subobject property

[importpylabs]: #/HowTo/ImportPyLabs
[importextension]: #/HowTo/ImportExtensionClass
[baseclass]: #/ExtendingPyLabs/BaseClasses
[contribute]: #/PyLabs50/Contributing


# CMDB Sub Object Specifications

A subobject is a complex property of CMDB Object. In the example below you find the specification file for configuring the subnet of a DHCP server.

## Content of the Specification File

* Import the required modules. Check [How to Import PyLabs][importpylabs] and [How to Import Classes from Extensions][importextension].
* Add a Class that inherits from the base class [CMDBObject][baseclass].
* Add all methods of the class.
* Add PyDocs for *each* method that gives its full explanation, see the *DocString* section in the [Contributing in Style page][contribute].


## Advantages

* The developer has immediately all modules that he has to use.
* The developer no longer has to take care of the documentation of the methods.
* The developer can immediately use the extension in the Q-Shell.


## Example

[[code]]
from pylabs import q
from pylabs.baseclasses.CMDBSubObject import CMDBSubObject

class DhcpSubnet(CMDBSubObject):
    """
    Collection of parameters for a full subnet.
    By default hosts in this subnet will us those parameters as their network settings
    """
    subnet = q.basetype.ipaddress(doc="subnet address of the subnet", allow_none=True)
    netmask = q.basetype.ipaddress(doc="netmask of the subnet", allow_none=True)
    domainNameServers = q.basetype.list(doc="domainnameserver for this subnet", allow_none=True)
    routers = q.basetype.list(doc="routers in this subnet", allow_none=True)
    nfsRootServer = q.basetype.ipaddress(doc="server to mount the root partition for a pxe boot", allow_none=True)
    pxeBootFile = q.basetype.string(doc="pxe boot file", allow_none=True)
    domainName = q.basetype.string(doc= "domainName of the subnet", allow_none=True)
    broadcastAddress = q.basetype.ipaddress(doc= "broadcast address for this subnet", allow_none=True) 
    
    def addRouter(self,router):
        """
        Add a router to the subnet
        @param router: IPv4Address of the router
        """
        pass

    def removeRouter(self,router):
        """
        Delete a router from the subnet
        @param router: IPv4Address from the router
        """
        pass

    def addDomainNameServer(self,domainnameserver):
        """
        Add a domainnameServer to the subnet
        @param domainnameserver: IPv4Address of the domainnameserver
        """
        pass

    def removeDomainNameServer(self,domainnameserver):
        """
        Delete a domainnameServer from the subnet
        @param domainnamesrver: IPv4Address of the domainnameserver
        """
        pass
                
    def __str__(self):
        """
        Print the subnet configuration in dhcpserver format
        """
        return self.subnet

    def __repr__(self):
        return self.__str__()


    def _buildConfigString(self):
        configLines = []
        configLines.append("    subnet %(subnet)s netmask %(mask)s \n   {"%{"subnet":self.subnet,"mask":self.netmask})
        
        if len(self.domainNameServers) > 0:
            dnsList = ", ".join(self.domainNameServers)
            configLines.append("        option domain-name-servers %s;"%dnsList)

        if len(self.routers) > 0:
            routerList = ", ".join(self.routers)
            configLines.append("        option routers %s;"%routerList)
        
        if self.pxeBootFile != None:
            configLines.append("        filename \"%s\";"%self.pxeBootFile)

        if self.nfsRootServer != None:
            configLines.append("        next-server %s;"%self.nfsRootServer)
        
        if self.broadcastAddress != None:
            configLines.append("        option broadcast-address %s;"%self.broadcastAddress)

        if self.domainName != None:
            configLines.append("        option domain-name \"%s\";"%self.domainName)

        configLines.append("    }")
        return "\n".join(configLines)

    def _printConfig(self):
        configLines = []
        configLines.append("    Subnet : %s"%self.subnet)
        configLines.append("    Netmask : %s"%self.netmask)
        
        if len(self.domainNameServers) > 0:
            dnsList = ", ".join(self.domainNameServers)
            configLines.append("    Domain name servers : %s"%dnsList)
        else:
            configLines.append("    Domain name servers : None")

        if len(self.routers) > 0:
            routerList = ", ".join(self.routers)
            configLines.append("    Routers : %s"%routerList)
        else:
            configLines.append("    Routers : None")
        
        configLines.append("    PXE Bootfile : %s"%self.pxeBootFile)
        configLines.append("    NFS RootServer : %s"%self.nfsRootServer)
        configLines.append("    Broadcast Address : %s;"%self.broadcastAddress)
        configLines.append("    Domain name : %s;"%self.domainName)               
        
        return "\n".join(configLines)
[[/code]]