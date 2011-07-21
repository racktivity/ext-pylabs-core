__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getPortData'
__priority__= 3

from pysnmp.entity.rfc3413.oneliner import cmdgen

OID_PORT_DATA = (1,3,6,1,4,1,13742,4,1,2,2,1)
OID_PORT_LABEL = OID_PORT_DATA + (2,)
OID_PORT_STATUS = OID_PORT_DATA + (3,)
OID_PORT_CURRENT = OID_PORT_DATA + (4,)
OID_PORT_MAX_CURRENT = OID_PORT_DATA + (5,)
OID_PORT_VOLTAGE = OID_PORT_DATA + (6,)
OID_PORT_ACTIVEPOWER = OID_PORT_DATA + (7,)
OID_PORT_APPARENTPOWER = OID_PORT_DATA + (8,)
OID_PORT_POWERFACTOR = OID_PORT_DATA + (9,)

def doSNMPgetnext(address, oid):
    errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().nextCmd(cmdgen.CommunityData('test-agent', 'public'),
                                      cmdgen.UdpTransportTarget(address),
                                      oid)
    
    if errorIndication or errorStatus:
        raise RuntimeError("Failed to do SNMP GETNEXT")
    
    return varBindTable

def doSNMPgetbulk(address, norepeaters=0, maxrepeats=1, *oid):
    errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().bulkCmd(cmdgen.CommunityData('test-agent', 'public'),
                                      cmdgen.UdpTransportTarget(address),
                                      norepeaters, maxrepeats, *oid)
    
    if errorIndication or errorStatus:
        raise RuntimeError("Failed to do SNMP GETNEXT")
    
    return varBindTable

def main(q, i, params, tags):
    ipaddress = params['deviceipaddress']
    apiport = params['deviceapiport']
    login = params['login']
    password = params['password']
    
    address = (ipaddress, apiport)
    
    deviceid = params['deviceid']
    datatype = params['datatype']
    
    if datatype not in ('PortState', 'StatePortCur',
            'Current','PortName','ApparentEnergy',
            'ActiveEnergy','Power', 'PowerFactor'):
        raise RuntimeError("Unsupported datatype '%s'" % datatype)
    
    portid = params['powerportid']

    oid_port_label = OID_PORT_LABEL + (portid - 1,)
    oid_port_status = OID_PORT_STATUS + (portid - 1,)
    oid_port_current = OID_PORT_CURRENT + (portid - 1,)
    oid_port_max_current = OID_PORT_MAX_CURRENT + (portid - 1,)
    oid_port_volatage = OID_PORT_VOLTAGE + (portid - 1,)
    oid_port_activepower = OID_PORT_ACTIVEPOWER + (portid - 1,)
    oid_port_apparentpower = OID_PORT_APPARENTPOWER + (portid - 1,)
    oid_port_powerfactor = OID_PORT_POWERFACTOR + (portid - 1,)
    
    data = doSNMPgetbulk(address, 8, 0, oid_port_label, oid_port_status,
                         oid_port_current, oid_port_max_current, oid_port_volatage, oid_port_activepower,
                         oid_port_apparentpower, oid_port_powerfactor)
    
    row = data[0]
    name = str(row[0][1])
    status = str(row[1][1])
    current = float(row[2][1]) / 1000
    maxCurrent = float(row[3][1]) / 1000
    voltage = float(row[4][1]) / 1000
    activepower = float(row[5][1])
    apparentpower = float(row[6][1])
    powerfactor = float(row[7][1])
    
    power = apparentpower * powerfactor
    
    status = status if status == 1 else 0
    
    port = {'PortState': bool(status),
            'StatePortCur': bool(status),
            'Current': current,
            'PortName': name,
            'ApparentEnergy': apparentpower,
            'ActiveEnergy': activepower,
            'Power': power,
            'PowerFactor': powerfactor,
            'sequence': portid}
    
    params['result'] = {'returncode': True, 'value': port[datatype]}

def match(q, i, params, tags):
    return params['devicetype'] == "raritan"

