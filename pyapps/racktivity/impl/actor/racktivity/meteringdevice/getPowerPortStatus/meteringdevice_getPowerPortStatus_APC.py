__author_ = 'racktivity'
__tags__ = 'meteringdevice', 'getPowerPortStatus'


from pysnmp.entity.rfc3413.oneliner import cmdgen

OID_VOLTAGE = (1,3,6,1,4,1,318,1,1,12,1,15)
OID_PORT_STATUS = (1,3,6,1,4,1,318,1,1,12,3,5,1,1,4)
OID_PORT_CURRENT = (1,3,6,1,4,1,318,1,1,12,3,5,1,1,7)
OID_PORT_NAME = (1,3,6,1,4,1,318,1,1,12,3,5,1,1,2)
OID_POWER_FACTOR = (1,3,6,1,4,1,318,1,1,12,1,17)
def doSNMPgetnext(ipaddress, oid):
    errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().nextCmd(cmdgen.CommunityData('test-agent', 'public'),
                                      cmdgen.UdpTransportTarget((ipaddress, 161)),
                                      oid)
    
    if errorIndication or errorStatus:
        raise RuntimeError("Failed to do SNMP GETNEXT")
    
    return varBindTable

def doSNMPgetbulk(ipaddress, norepeaters=0, maxrepeats=1, *oid):
    errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().bulkCmd(cmdgen.CommunityData('test-agent', 'public'),
                                      cmdgen.UdpTransportTarget((ipaddress, 161)),
                                      norepeaters, maxrepeats, *oid)
    
    if errorIndication or errorStatus:
        raise RuntimeError("Failed to do SNMP GETNEXT")
    
    return varBindTable

def main(q, i, params, tags):
    ipaddress = params['deviceipaddress']
    apiport = params['deviceapiport']
    login = params['login']
    password = params['password']
    
    deviceid = params['deviceid']
    portid = params['portid']
    
    oid_status = OID_PORT_STATUS + (portid - 1,)
    oid_current = OID_PORT_CURRENT + (portid - 1,)
    oid_name = OID_PORT_NAME + (portid - 1,)
    
    data = doSNMPgetbulk(ipaddress, 5, 0, OID_VOLTAGE, oid_status, oid_name, oid_current, OID_POWER_FACTOR)
    
    row = data[0]
    voltage = float(row[0][1])
    status = float(row[1][1])
    name = str(row[2][1])
    current = float(row[3][1])
    powerfactor = float(row[4][1])
    
    apparentEnergy = current * voltage
    power = apparentEnergy * powerfactor
    activeEnergy = power
    
    status = status if status == 1 else 0
    
    port = {'PortState': bool(status),
            'StatePortCur': bool(status),
            'Current': current,
            'PortName': name,
            'ApparentEnergy': apparentEnergy,
            'ActiveEnergy': activeEnergy,
            'Power': power,
            'PowerFactor': powerfactor,
            'sequence': portid}
    
    params['result'] = {'returncode': True, 'status': port['PortState']}
    
def match(q, i, params, tags):
    return params['devicetype'] == "apc"
