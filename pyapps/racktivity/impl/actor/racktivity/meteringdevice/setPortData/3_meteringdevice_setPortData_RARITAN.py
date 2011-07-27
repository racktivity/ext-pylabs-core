__author__ = 'racktivity'


from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

OID_PORT_DATA = (1,3,6,1,4,1,13742,4,1,2,2,1)
OID_PORT_LABEL = OID_PORT_DATA + (2,)

def doSNMPset(address, password, oid, value):
    errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('test-agent', password),
                                      cmdgen.UdpTransportTarget(address),
                                      (oid, value))
    
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
    datavalue = params['datavalue']
    
    if datatype not in ('PortName',):
        raise RuntimeError("Unsupported datatype '%s'" % datatype)
    
    portid = params['powerportid']
    
    oid_port_label = OID_PORT_LABEL + (portid,)
    doSNMPset(address, password, oid_port_label, rfc1902.OctetString(datavalue))
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return params['devicetype'] == "raritan"

