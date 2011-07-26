__author__ = 'racktivity'

from pysnmp.entity.rfc3413.oneliner import cmdgen

OID_POWER = (1,3,6,1,4,1,318,1,1,12,1,16)
OID_POWER_FACTOR = (1,3,6,1,4,1,318,1,1,12,1,17)
OID_POWER_APPARENT = (1,3,6,1,4,1,318,1,1,12,1,18)
OID_NUMBER_PORTS = (1,3,6,1,4,1,318,1,1,12,3,1,4)
OID_VOLTAGE = (1,3,6,1,4,1,318,1,1,12,1,15)
OID_HW_REV = (1,3,6,1,4,1,318,1,1,12,1,2)
OID_SW_REV = (1,3,6,1,4,1,318,1,1,12,1,3)

OID_PORT_STATUS = (1,3,6,1,4,1,318,1,1,12,3,5,1,1,4)
OID_PORT_CURRENT = (1,3,6,1,4,1,318,1,1,12,3,5,1,1,7)
OID_PORT_NAME = (1,3,6,1,4,1,318,1,1,12,3,5,1,1,2)

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
    port = params['deviceapiport']
    login = params['login']
    password = params['password']
    
    #deviceid = params['deviceid']
    #datatype = params['datatype']
    
    data = doSNMPgetbulk(ipaddress, 7, 0, OID_POWER, OID_POWER_FACTOR, OID_POWER_APPARENT, OID_VOLTAGE, OID_NUMBER_PORTS,
                         OID_HW_REV, OID_SW_REV)
    
    totalPower = float(data[0][0][1])
    totalPowerFactor = float(data[0][1][1]) / 1000.0
    totalApparentPower = float(data[0][2][1])
    voltage = float(data[0][3][1])
    numberOfPorts = float(data[0][4][1])
    hw_rev = str(data[0][5][1])
    sw_rev = str(data[0][6][1])
    
    totalCurrent = 0
    data = doSNMPgetbulk(ipaddress, 0, numberOfPorts, OID_PORT_STATUS, OID_PORT_CURRENT, OID_PORT_NAME)
    
    result = dict()
    result['Ports'] = list()
    ports = list()
    for i in range(numberOfPorts):
        rec = data[i]
        
        status = int(rec[0][1])
        current = float(rec[1][1])
        totalCurrent += current
        name = str(rec[2][1])
        apparentEnergy = current * voltage
        power = apparentEnergy * totalPowerFactor
        activeEnergy = power
        status = status if status == 1 else 0
        port = {'PortState': bool(status),
                'StatePortCur': bool(status),
                'Current': current,
                'PortName': name,
                'ApparentEnergy': apparentEnergy,
                'ActiveEnergy': activeEnergy,
                'Power': power,
                'PowerFactor': totalPowerFactor,
                'sequence': i + 1}
        ports.append(port)
    
    for port in ports:
        for k in port.keys():
            v = port[k]
            if isinstance(v, bool):
                port['%sTxt' % k] = "On" if v else "Off"
            elif isinstance(v, float):
                port['%sTxt' % k] = "%0.1f" % v
            
    result['Ports'] = ports
    result['Voltage'] = voltage
    result['HardwareVersion'] = hw_rev
    result['FirmwareVersion'] = sw_rev
    result['TotalPower'] = totalPower
    result['TotalRealPower'] = totalPower
    result['TotalPowerFactor'] = totalPowerFactor
    result['TotalApparentEnergy'] = totalApparentPower
    result['TotalActiveEnergy'] = totalPower
    result['TotalCurrent'] = totalCurrent
    result['Frequency'] = 0.0
    
    for k in result.keys():
        v = result[k]
        if isinstance(v, bool):
            result['%sTxt' % k] = "On" if v else "Off"
        elif isinstance(v, float):
            result['%sTxt' % k] = "%0.1f" % v
    
    params['result'] = {'returncode': True,
                        'value': result}

def match(q, i, params, tags):
    return params['devicetype'] == "apc"
