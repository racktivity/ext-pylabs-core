__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getDeviceData'
__priority__= 3

import collections

ERR_INDEX_OUT_OF_RANGE = 8

POINTER_POWER_ATTRS = ("Voltage",
                        "MaxVoltage",
                        "MinVoltage",
                        "TotalCurrent",
                        "MaxTotalCurrent",
                        "MinTotalCurrent",
                        "TotalRealPower",
                        "MaxTotalPower",
                        "MinTotalPower",
                        "TotalActiveEnergy",
                        "TotalApparentEnergy",
                        "Frequency",
                        "TotalPowerFactor",
                        "MaxTotalPowerFactor",
                        "MinTotalPowerFactor")

POINTER_POWER_PORT_ATTRS = ("Current",
                            "MaxCurrent",
                            "MinCurrent",
                            "Power",
                            "MaxPower",
                            "MinPower",
                            "ActiveEnergy",
                            "ApparentEnergy",
                            "ApparentPower",
                            "PowerFactor",
                            "MaxPowerFactor",
                            "MinPowerFactor",
                            "PortName",
                            "StatePortCur")

POINTER_MASTER_ATTRS = ("DHCPEnable",
                        "ModuleName",
                        "FirmwareVersion",
                        "HardwareVersion",
                        "SNMPTrapRecvIP",
                        "SNMPTrapRecvPort",
                        "SNMPCommunityRead",
                        "SNMPCommunityWrite",
                        "IPAddress",
                        "SubNetMask",
                        "StdGateWay",
                        "DnsServer",
                        "NTPServer",
                        "MAC",
                        "FirmwareID",
                        "HardwareID")

#some binary data that we don't need
SKIP_KEYS = ("Eeprom",
            "VoltageBuffer",
            "CurrentBuffer")


def getAttribute(client, deviceid, datatype):
    methodname = "get%s" % datatype
    method = getattr(client, methodname)
    return method(deviceid)

def getPowerAttribute(client, deviceid, datatype):
    methodname = "get%s" % datatype
    method = getattr(client.power, methodname)
    return method(deviceid)

def getMasterAttribute(client, datatype):
    methodname = "get%s" % datatype
    method = getattr(client.master, methodname)
    return method()

def getPortsAttribute(client, deviceid, length, datatype):
    methodname = "get%s" % datatype
    method = getattr(client.power, methodname)
    return method(deviceid, 1, length)

def getStrRepr(value):
    if isinstance(value, bool):
        return "On" if value else "Off"
    elif isinstance(value, (int, float)):
        return "%0.1f" % value
    else:
        return value
def isConvertable(value):
    return isinstance(value, (int, float, bool))

def guessPortCount(client):
    for index in [64, 32, 16, 8]:
        code, value = client.power.getPortName('P1', index)
        if code == 0:
            return index
    return 0
    
def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    datatype = params['datatype']
    
    if datatype.lower() == 'all':
        #collecting all data from all modules.
        values = dict()
        portsdict = collections.defaultdict(dict)
        
        for attr in POINTER_MASTER_ATTRS:
            code, value = getMasterAttribute(rackclient, attr)
            value = value[0] if isinstance(value, tuple) else value
            if code == 0:
                values[attr] = value
                if isConvertable(value):
                    values["%sTxt" % attr] = getStrRepr(value)
        
        for attr in POINTER_POWER_ATTRS:
            code, value = getPowerAttribute(rackclient, 'P1', attr)
            value = value[0] if isinstance(value, tuple) else value
            if 'PowerFactor' in attr:
                value = value / 100.0
            if code == 0:
                values[attr] = value
                if isConvertable(value):
                    values["%sTxt" % attr] = getStrRepr(value)
                    
        portCount = guessPortCount(rackclient)
        
        for attr in POINTER_POWER_PORT_ATTRS:
            code, portvalues = getPortsAttribute(rackclient, 'P1', portCount, attr)
            for i, value in enumerate(portvalues):
                value = value[0] if isinstance(value, tuple) else value
                if 'PowerFactor' in attr:
                    value = value / 100.0
                portsdict[i][attr] = value
                if isConvertable(value):
                    portsdict[i]["%sTxt" % attr] = getStrRepr(value)
                    
        ports = list()
        for i in range(len(portsdict)):
            port = portsdict[i]
            port['sequence'] = i + 1
            ports.append(port)
        
        values['TotalPower'] = values['TotalRealPower']
        values['TotalPowerTxt'] = getStrRepr(values['TotalRealPower'])
        values['Ports'] = ports
        params['result'] = {'returncode': True, 'value': values}
    else:
        data = None
        errorcode = 0
        if deviceid.startswith('M'):
            errorcode, data = getMasterAttribute(rackclient, datatype)
        elif deviceid.startswith('P'):
            errorcode, data = getPowerAttribute(rackclient, deviceid, datatype)
        else:
            raise RuntimeException("Wrong device id, it must start with either M, or P")
        
        params['result'] = {'returncode': not bool(errorcode), 'value': data}


def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"

