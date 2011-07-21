__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'setPortData'
__priority__= 3

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

OID_PORT_NAME = (1,3,6,1,4,1,318,1,1,12,3,4,1,1,2)

def doSNMPset(address, password, oid, value):
    errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('test-agent', password),
                                      cmdgen.UdpTransportTarget(address),
                                      (oid, value))
    
    if errorIndication or errorStatus:
        raise RuntimeError("Failed to do SNMP SET")
    
    return varBindTable

def main(q, i, params, tags):
    ipaddress = params['deviceipaddress']
    apiport = params['deviceapiport']
    login = params['login']
    password = params['password']
    
    deviceid = params['deviceid']
    datatype = params['datatype']
    datavalue = params['datavalue']
    
    if datatype not in ('PortName',):
        raise RuntimeError("Unsupported datatype '%s'" % datatype)
    
    portid = params['powerportid']
    address = (ipaddress, apiport)
    
    oid_name = OID_PORT_NAME + (portid,)
    doSNMPset(address, password, oid_name, rfc1902.OctetString(datavalue))
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return params['devicetype'] == "apc"

