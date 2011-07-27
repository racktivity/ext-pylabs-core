__author_ = 'racktivity'

from pysnmp.entity.rfc3413.oneliner import cmdgen
OID_PORT_CMD = (1,3,6,1,4,1,13742,4,1,2,2,1,3)
from pysnmp.proto import rfc1902

def doSNMPset(address, oid, value):
    errorIndication, errorStatus, errorIndex, varBindTable = cmdgen.CommandGenerator().setCmd(cmdgen.CommunityData('test-agent', 'private'),
                                      cmdgen.UdpTransportTarget(address),
                                      (oid, value))
    
    if errorIndication or errorStatus:
        raise RuntimeError("Failed to do SNMP GETNEXT")
    
    return varBindTable

def main(q, i, params, tags):
    ipaddress = params['deviceipaddress']
    port = params['deviceapiport']
    login = params['login']
    password = params['password']
    
    address = (ipaddress, port)
    deviceid = params['deviceid']
    portid = params['portid']
    
    doSNMPset(address, OID_PORT_CMD + (portid,), rfc1902.Integer(1))
    
def match(q, i, params, tags):
    return params['devicetype'] == "raritan"
