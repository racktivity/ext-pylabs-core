from pymonkey.baseclasses.BaseEnumeration import BaseEnumeration
from pymonkey.baseclasses.BaseEnumeration import EnumerationWithValue

# @doc None
class applicationstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('ACTIVE')
        cls.registerItem('DISABLED')
        cls.registerItem('HALTED')
        cls.registerItem('MAINTENANCE')
        cls.registerItem('BLACKLISTED')
        cls.registerItem('FULL')
        cls.registerItem('ABANDONED')
        cls.registerItem('STARTING')
        cls.registerItem('STOPPING')
        cls.registerItem('CONFIGURED')
        cls.finishItemRegistration()

# @doc None
class applicationaccounttype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('SYSTEMACCOUNT')
        cls.registerItem('PUBLICACCOUNT')
        cls.finishItemRegistration()

class applicationmodetype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('READONLY')
        cls.registerItem('READWRITE')
        cls.registerItem('WRITEONLY')
        cls.finishItemRegistration()


# @doc None
class applicationipprotocoltype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('TCP')
        cls.registerItem('UDP')
        cls.finishItemRegistration()
        
class applicationinstalllimitationtype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('NONE')
        cls.registerItem('MACHINE')
        cls.registerItem('CLOUDSPACE')
        cls.registerItem('CLOUD')
        cls.finishItemRegistration()
        

# @doc None
class backplanetype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('INFINIBAND')
        cls.registerItem('ETHERNET')
        cls.finishItemRegistration()
        

# @doc type of physical cable
class cabletype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('USBCABLE')
        cls.registerItem('FIREWIRECABLE')
        cls.registerItem('NETCABLE')
        cls.registerItem('IBCABLE')
        cls.registerItem('SATACABLE')
        cls.registerItem('SERIALCABLE')
        cls.registerItem('POWERCABLE')
        cls.finishItemRegistration()

# @doc None
class cloudspacestatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('ACTIVE')
        cls.registerItem('DISABLED')
        cls.finishItemRegistration()


# @doc None
class clouduserstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('CONFIGURED')
        cls.registerItem('CREATED')
        cls.registerItem('DISABLED')
        cls.finishItemRegistration()
        
# @doc None
class customerstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('CONFIGURED')
        cls.registerItem('ACTIVE')
        cls.registerItem('DISABLED')
        cls.finishItemRegistration()
        
# @doc device status
class devicestatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('BROKEN')
        cls.registerItem('ACTIVE')
        cls.registerItem('SLEEPING')
        cls.registerItem('INREPAIR')
        cls.registerItem('INSTOCK')
        cls.finishItemRegistration()


# @doc physical disk interface type
class diskinterfacetype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('SAS')
        cls.registerItem('SATA')
        cls.registerItem('SCSI')
        cls.registerItem('FC')
        cls.finishItemRegistration()


# @doc disk status
class devicediskstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('BROKEN')
        cls.registerItem('ACTIVE')
        cls.registerItem('SLEEPING')
        cls.registerItem('INSTOCK')
        cls.finishItemRegistration()


# @doc type of physical network interface
class nicporttype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('ETHERNET_10MB')
        cls.registerItem('ETHERNET_100MB')
        cls.registerItem('ETHERNET_GB')
        cls.registerItem('ETHERNET_10GB')
        cls.registerItem('INFINIBAND')
        cls.registerItem('FC')
        cls.finishItemRegistration()


# @doc status of physical network interface
class nicportstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('BROKEN')
        cls.registerItem('ACTIVE')
        cls.registerItem('NOTCONNECTED')
        cls.finishItemRegistration()


# @doc component type
class componenttype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('SWC')
        cls.registerItem('PWC')
        cls.registerItem('NIC')
        cls.registerItem('USPC')
        cls.registerItem('CPU')
        cls.registerItem('MB')
        cls.registerItem('HDD')
        cls.registerItem('MEM')
        cls.finishItemRegistration()


# @doc device type
class devicetype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('AIRCO')
        cls.registerItem('COMPUTER')
        cls.registerItem('POWERSWITCH')
        cls.registerItem('SWITCH')
        cls.registerItem('UPS')
        cls.registerItem('POOL')
        cls.registerItem('SMARTCLIENT')
        cls.finishItemRegistration()


# @doc None
class deviceaccounttype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('BIOSACCOUNT')
        cls.finishItemRegistration()


# @doc status of physical power port
class powerportstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('BROKEN')
        cls.registerItem('ACTIVE')
        cls.registerItem('NOTCONNECTED')
        cls.finishItemRegistration()
        

# @doc status of physical power port
class feedConnectorStatusType(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('BROKEN')
        cls.registerItem('ACTIVE')
        cls.registerItem('NOTCONNECTED')
        cls.finishItemRegistration()

class feedProductionType(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('COAL')
        cls.registerItem('GENERIC')
        cls.registerItem('NUCLEAR')
        cls.registerItem('GAS')
        cls.registerItem('GENERIC_GREEN')
        cls.registerItem('WIND')
        cls.registerItem('SOLAR')
        cls.registerItem('GENERIC_FOSSILE')
        


# @doc None
class iptype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('STATIC')
        cls.registerItem('DHCP')
        cls.finishItemRegistration()


# @doc None
class ipversion(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('IPV4')
        cls.registerItem('IPV6')
        cls.finishItemRegistration()

# @doc None
class ipstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('ACTIVE')
        cls.registerItem('TODELETE')
        cls.registerItem('CONFIGURED')
        cls.registerItem('DISABLED')
        cls.finishItemRegistration()

# @doc status of lan
class lanstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('BROKEN')
        cls.registerItem('ACTIVE')
        cls.registerItem('DISABLED')
        cls.registerItem('NOTCONNECTED')
        cls.finishItemRegistration()

# @doc None
class lantype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('STATIC')
        cls.registerItem('DYNAMIC')
        cls.finishItemRegistration()
        

class meteringdeviceconfigstatus(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('IDENTIFIED')
        cls.registerItem('CONFIGURED')
        cls.registerItem('USED')
        cls.finishItemRegistration()

class meteringdevicetype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('PM0816_ZB')
        cls.registerItem('PM0816')
        cls.registerItem('PM0816_ZB_S10')
        cls.registerItem('PM0816_S10')
        cls.registerItem('AP7951')
        cls.registerItem('RARITAN')
        cls.finishItemRegistration()
    
# @doc None
class porttype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('SERIAL')
        cls.registerItem('ZIGBEE')
        cls.finishItemRegistration()

class sensortype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('AIRFLOWSENSOR')
        cls.registerItem('HUMIDITYSENSOR')
        cls.registerItem('TEMPERATURESENSOR')
        cls.finishItemRegistration()

# @doc None
class meteringdeviceeventlevel(EnumerationWithValue):
    @classmethod
    def _initItems(cls):
            cls.registerItem('UNKNOWN', 0)
            cls.registerItem('CRITICAL', 1)
            cls.registerItem('URGENT', 2)
            cls.registerItem('ERROR', 3)
            cls.registerItem('WARNING', 4)
            cls.registerItem('INFO', 5)
            cls.finishItemRegistration()

# @doc None
class policystatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('ACTIVE')
        cls.registerItem('DISABLED')
        cls.finishItemRegistration()
        

# @doc None
class racktype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('CLOSED')
        cls.registerItem('CLOSEDCOOLED')
        cls.registerItem('OPEN')
        cls.finishItemRegistration()

# @doc type of network interface
class nictype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('ETHERNET_10MB')
        cls.registerItem('ETHERNET_100MB')
        cls.registerItem('ETHERNET_GB')
        cls.registerItem('ETHERNET_10GB')
        cls.registerItem('INFINIBAND')
        cls.registerItem('FC')
        cls.finishItemRegistration()

# @doc status of network interface
class nicstatustype(BaseEnumeration):
    @classmethod
    def _initItems(cls):
        cls.registerItem('BROKEN')
        cls.registerItem('ACTIVE')
        cls.registerItem('DISABLED')
        cls.registerItem('NOTCONNECTED')
        cls.registerItem('TODELETE')
        cls.finishItemRegistration()
