__author__ = 'aserver'
__tags__ = 'rack', 'discover'
__priority__= 3

from pylabs.pmtypes import IPv4Range, IPv4Address
from pysnmp.entity.rfc3413.oneliner import cmdgen
from racktivity_mibs import racktivity_mib
import pysnmp.proto


class snmpModule(object):
    SYS_OBJECTID = (1,3,6,1,2,1,1,2,0)
    
    def __init__(self, password, port, q):
        self.password = password
        self.port = port
        self.q = q
        
    def doSNMPgetnext(self, ipaddress, oid):
        errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().nextCmd(cmdgen.CommunityData('test-agent', self.password),
                                          cmdgen.UdpTransportTarget((ipaddress, self.port)),
                                          oid)
        
        if errorIndication or errorStatus:
            raise RuntimeError("Failed to do SNMP GETNEXT")
        
        return varBindTable
    
    def doSNMPget(self, ipaddress, oid):
        errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().getCmd(cmdgen.CommunityData('test-agent', self.password),
                                          cmdgen.UdpTransportTarget((ipaddress, self.port)),
                                          oid)
        
        if errorIndication or errorStatus:
            raise RuntimeError("Failed to do SNMP GET")
        
        return varBindTable
    
    def discoverIp(self, ipaddress):
        try:
            device_id = tuple(self.doSNMPget(ipaddress, self.SYS_OBJECTID)[0][1])
            return ".".join(tuple(str(c) for c in device_id[6:]))
        except:
            return
    
    def discoverIpRange(self, startip, stopip, excludedIPs = list()):
        result = list()
        range = IPv4Range(startip, stopip)
        ip = range.fromIp
        while ip <= range.toIp:
            ipaddress = str(ip)
            ip += 1 #increment
            if ipaddress in excludedIPs:
                continue
            devid = self.discoverIp(ipaddress)
            if not devid:
                continue
            result.append((ipaddress, devid))
        return result

    def getDevicePorts(self, address, OID):
        table = self.doSNMPgetnext(address, OID)
        ports_list = list()
        for records in table:
            for key, value in records:
                ports_list.append(str(value))
        return ports_list
    
    def oid2tuple(self, oid):
        r = list()
        for item in oid.split("."):
            r.append(int(item))
        return tuple(r)
    
    def getDeviceData(self, address, sysobjectid):
        q = self.q
        q.logger.log("Discovery: getting info of device %s with id %s"%(address, sysobjectid))
        #Do I have info for this device?
        guids = q.actions.rootobject.autodiscoverysnmpmap.find(sysobjectid = str(sysobjectid))["result"]["guidlist"]
        if not guids:
            q.logger.log("Discovery: Device with sysobjectid %s is not supported"%sysobjectid)
            return None
        snmpInfo = q.actions.rootobject.autodiscoverysnmpmap.getObject(guids[0])
        oids = snmpInfo.oidmapping
        
        #fill predefined/default info
        device = {"type":snmpInfo.manufacturer, "product":"Unknown", "power_ports":[],"sensor_ports":[]}
        
        if "device_name" in oids:
            device['product'] = str(self.doSNMPget(address, self.oid2tuple(oids["device_name"]))[0][1])
        
        if "power_ports" in oids:
            portsnames = self.getDevicePorts(address, self.oid2tuple(oids["power_ports"]))
            device['power_ports'] = [{'label': label, 'sequence': index + 1} for index, label in enumerate(portsnames)]
        
        if "sensor_ports" in oids:
            portsnames = getDevicePorts(address, self.oid2tuple(oids["sensor_ports"]))
            device['sensor_ports'] = [{'label': label, 'sequence': index + 1} for index, label in enumerate(portsnames)]
        
        return device


def configureMD(q, address, data, replace, request):
    ipguids = q.actions.rootobject.ipaddress.find(address=address)['result']['guidlist']
    if ipguids:
        if replace:
            mdguids = q.actions.rootobject.meteringdevice.find(ipaddressguid = ipguids[0])["result"]["guidlist"]
            for guid in mdguids:
                q.actions.rootobject.meteringdevice.delete(guid, request = request)
        else:
            q.logger.log("autodiscovery: IP address already used, skipping ..")
            return
    
    productName = data["product"]
    rackguid = data["rackguid"]
    port = data["port"]
    ipaddressguid = q.actions.rootobject.ipaddress.create(name=address, address=address, request = request)['result']['ipaddressguid']

    #model master module.
    masterguid = q.actions.rootobject.meteringdevice.create(name="%s-%s" % (productName, address),
                                   id='M1',
                                   meteringdevicetype=data["type"],
                                   template=False,
                                   rackguid=rackguid,
                                   attributes = {'deviceapiportnr': str(port)},
                                   nicinfo = [{'ipaddressguids':[ipaddressguid], 'status':str(q.enumerators.nicstatustype.ACTIVE),
                                               'nictype':str(q.enumerators.nictype.ETHERNET_GB), 'order':0}],
                                   meteringdeviceconfigstatus=str(q.enumerators.meteringdeviceconfigstatus.IDENTIFIED),
                                   request = request,
                                   )['result']['meteringdeviceguid']
    #model power module.
    q.actions.rootobject.meteringdevice.create(name="%s-%s-P1" % (productName, address),
                                   id='P1',
                                   meteringdevicetype=data["type"],
                                   template=False,
                                   rackguid=rackguid,
                                   parentmeteringdeviceguid=masterguid,
                                   poweroutputinfo=data["power_ports"],
                                   meteringdeviceconfigstatus=str(q.enumerators.meteringdeviceconfigstatus.IDENTIFIED),
                                   request = request
                                   )
    
    #model temperature module.
    q.actions.rootobject.meteringdevice.create(name="%s-%s-T1" % (productName, address),
                                   id='T1',
                                   meteringdevicetype=data["type"],
                                   template=False,
                                   rackguid=rackguid,
                                   parentmeteringdeviceguid=masterguid,
                                   sensorinfo=data["sensor_ports"],
                                   meteringdeviceconfigstatus=str(q.enumerators.meteringdeviceconfigstatus.IDENTIFIED),
                                   request = request
                                   )

def main(q, i, params, tags):
    ips = params["ipaddresslist"]
    rackguid = params["rackguid"]
    port = params["port"]
    password = params["password"]
    updateExisting = params["updateExisting"]
    snmpobj = snmpModule(password, port, q)
    ipsinfo = dict()
    for ip in ips:
        if ip.find(":") > 0:
            #This is a range
            startip, endip = ip.split(":", 1)
            ipsinfo.update(snmpobj.discoverIpRange(startip, endip))
        else:
            devid = snmpobj.discoverIp(ip)
            if devid:
                ipsinfo[ip] = devid
    
    #get the information of each discovered device
    for ip in ipsinfo:
        q.logger.log("Discovery: discovered device with IP %s"%ip)
        info = snmpobj.getDeviceData(ip, ipsinfo[ip])
        if not info:
            ipsinfo[ip] = {"type":"unknown"}
            continue #Undefined type
        info["rackguid"] = rackguid
        info["port"] = port
        ipsinfo[ip] = info
        configureMD(q, ip, info, updateExisting, params["request"])
    
    params["result"] = {"returncode":True, "discovered":ipsinfo}

def match(q, i, params, tags):
    return True
