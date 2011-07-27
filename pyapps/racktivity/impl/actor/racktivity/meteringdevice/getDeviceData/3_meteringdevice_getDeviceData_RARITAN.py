__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getDeviceData'
__priority__= 3

from pysnmp.entity.rfc3413.oneliner import cmdgen

OID_SW_REV = (1,3,6,1,4,1,13742,4,1,1,1)
OID_HW_REV = (1,3,6,1,4,1,13742,4,1,1,7)
OID_VOLTAGE = (1,3,6,1,4,1,13742,4,1,6,2,1,3)
OID_PORT_COUNT = (1,3,6,1,4,1,13742,4,1,2,1)

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
    port = params['deviceapiport']
    login = params['login']
    password = params['password']
    
    address = (ipaddress, port)
    #deviceid = params['deviceid']
    #datatype = params['datatype']
    
    data = doSNMPgetbulk(address, 4, 0, OID_SW_REV, OID_HW_REV, OID_VOLTAGE, OID_PORT_COUNT)
    
    sw_rev = str(data[0][0][1])
    hw_rev = str(data[0][1][1])
    voltage = float(data[0][2][1]) / 1000
    numberOfPorts = int(data[0][3][1])
    
    data = doSNMPgetbulk(address, 0, numberOfPorts, OID_PORT_LABEL, OID_PORT_STATUS,
                  OID_PORT_CURRENT, OID_PORT_MAX_CURRENT, OID_PORT_VOLTAGE,
                  OID_PORT_ACTIVEPOWER, OID_PORT_APPARENTPOWER, OID_PORT_POWERFACTOR)
    
    totalCurrent = 0
    totalPower = 0
    totalApparentPower = 0
    totalActivePower = 0
    
    result = dict()
    result['Ports'] = list()
    
    ports = list()
    for i in range(numberOfPorts):
        rec = data[i]
        name = str(rec[0][1])
        status = int(rec[1][1])
        current = float(rec[2][1]) / 1000.0
        maxCurrent = float(rec[3][1]) / 1000.0
        portVoltage = float(rec[4][1]) / 1000.0
        activePower = float(rec[5][1])
        apparentPower = float(rec[6][1])
        powerfactor = float(rec[7][1]) / 100.0
        
        
        power = apparentPower * powerfactor
        
        totalCurrent += current
        totalPower += power
        totalApparentPower += apparentPower
        totalActivePower += activePower
        
        status = status if status == 1 else 0
        port = {'PortState': bool(status),
                'StatePortCur': bool(status),
                'Current': current,
                'PortName': name,
                'ApparentEnergy': apparentPower,
                'ActiveEnergy': activePower,
                'Power': power,
                'PowerFactor': powerfactor,
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
    result['TotalPowerFactor'] = totalPower / totalApparentPower if totalApparentPower else 0.0
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
    return params['devicetype'] == "raritan"
