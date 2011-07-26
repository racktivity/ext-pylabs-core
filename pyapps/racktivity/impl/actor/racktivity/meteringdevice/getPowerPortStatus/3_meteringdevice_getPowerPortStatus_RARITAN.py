__author__ = 'racktivity'

from pysnmp.entity.rfc3413.oneliner import cmdgen

OID_PORT_DATA = (1,3,6,1,4,1,13742,4,1,2,2,1)
OID_PORT_STATUS = OID_PORT_DATA + (3,)

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
    
    portid = params['portid']
    
    oid_port_status = OID_PORT_STATUS + (portid - 1,)
    
    data = doSNMPgetbulk(address, 1, 0, oid_port_status)
    
    row = data[0]
    status = int(row[0][1])
    status = status if status == 1 else 0
    
    params['result'] = {'returncode': True, 'status': bool(status)}

def match(q, i, params, tags):
    return params['devicetype'] == "raritan"

