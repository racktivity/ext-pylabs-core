__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getDeviceData'
__priority__= 3

import collections

ERR_INDEX_OUT_OF_RANGE = 8

POINTER_POWER_MONITOR_MAP = ("ActiveEnergy",
                    "Voltage",
                    "ApparentEnergy",
                    "Power",
                    "StatePortCur",
                    "Current",
                    "MaxCurrent",
                    "MaxPower",
                    "MaxTotalCurrent",
                    "MaxTotalPower",
                    "MaxVoltage",
                    "MaxVoltageWarning",
                    "MinVoltage",
                    "Frequency",
                    
                    "TotalCurrent",
                    "TotalPower",
                    "TotalPowerFactor",
                    "TotalApparentEnergy",
                    "TotalActiveEnergy")

POINTER_POWER_SETTING_MAP = ("Address",
                    "TimeTillLastSnapshot",
                    "FirmwareVersion",
                    "HardwareVersion",
                    "OperationMode",
                    "FactoryModePassword",
                    "CurrentPriorOff",
                    "DelayOn",
                    "FirmwareID",
                    "HardwareID",
                    "MaxCurrentOff",
                    "MaxCurrentWarning",
                    "MaxPowerOff",
                    "MaxPowerWarning",
                    "MaxTotalCurrentOff",
                    "MaxTotalCurrentWarning",
                    "MaxTotalPowerOff",
                    "MaxTotalPowerWarning",
                    "MaxVoltageOff",
                    "MinVoltageOff",
                    "MinVoltageWarning",
                    "ModuleID",
                    "PortName",
                    "PortState",
                    "Monitor",
                    "Setting",
                    "Eeprom",
                    "VoltageBuffer",
                    "CurrentBuffer",
                    "CurrentOffset",
                    "RelaisDelayON",
                    "RelaisDelayOFF",
                    "VoltageFactor",
                    "FrequencySpec",
                    "CurrentFactor",
                    "PowerFactor",
                    "PowerCheckOffset",
                    "AddressMode")

POINTER_MASTER_SETTING_MAP = ("DHCPEnable",
                    "ModuleName",
                    "Login",
                    "Password",
                    "FirmwareVersion",
                    "HardwareVersion",
                    "SNMPTrapIP",
                    "IPAddress",
                    "SubNetMask",
                    "StdGateWay",
                    "DnsServer",
                    "NTPServer",
                    "MAC",
                    "OperationMode",
                    "FactoryModePassword",
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

def getPortAttribute(client, deviceid, portid, datatype):
    methodname = "get%s" % datatype
    method = getattr(client.power, methodname, portid)
    return method(deviceid, portid)

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    datatype = params['datatype']
    
    if datatype.lower() == 'all':
        #collecting all data from all modules.
        value = dict()
        portsdict = collections.defaultdict(dict)
        #get the setting attribute.
        code, masterSetting = rackclient.master.getSetting()
        if code != 0:
            raise RuntimeError("Failed to get device 'Setting' on master errorcode: %s" % code)
        
        def master_setting_map((i, v)):
            return (POINTER_MASTER_SETTING_MAP[i], v)
        value.update(map(master_setting_map, enumerate(masterSetting)))
        
        code, powerSetting = rackclient.power.getSetting('P1')
        if code != 0:
            raise RuntimeError("Failed to get device 'Setting' on P1 errorcode: %s" % code)
        
        for index, v in enumerate(powerSetting):
            attrname = POINTER_POWER_SETTING_MAP[index]
            if attrname in SKIP_KEYS:
                continue
            if isinstance(v, list):
                for subindex, pv in enumerate(v):
                    portsdict[subindex][attrname] = pv
                    if isinstance(pv, bool):
                        portsdict[subindex]["%sTxt" % attrname] = "On" if pv else "Off"
                    elif isinstance(pv, (int, float)):
                        portsdict[subindex]["%sTxt" % attrname] = "%0.1f" % pv
            else:
                value[attrname] = v
                if isinstance(v, bool):
                    value["%sTxt" % attrname] = "On" if v else "Off"
                elif isinstance(v, (int, float)):
                    value["%sTxt" % attrname] = "%0.1f" % v
                
        code, powerMonitor = rackclient.power.getMonitor('P1')
        if code != 0:
            raise RuntimeError("Failed to get device 'Monitor' on P1 errorcode: %s" % code)
        
        for index, v in enumerate(powerMonitor):
            attrname = POINTER_POWER_MONITOR_MAP[index]
            if isinstance(v, list):
                for subindex, pv in enumerate(v):
                    portsdict[subindex][attrname] = pv
                    if isinstance(pv, bool):
                        portsdict[subindex]["%sTxt" % attrname] = "On" if pv else "Off"
                    elif isinstance(pv, (int, float)):
                        portsdict[subindex]["%sTxt" % attrname] = "%0.1f" % pv
                    
            else:
                value[attrname] = v
                if isinstance(v, bool):
                    value["%sTxt" % attrname] = "On" if v else "Off"
                elif isinstance(v, (int, float)):
                    value["%sTxt" % attrname] = "%0.1f" % v
        
        #put the ports in a normal list (instead of a default dict)
        #and retain the order
        ports = list()
        for i in range(len(portsdict)):
            port = portsdict[i]
            port['sequence'] = i + 1
            ports.append(port)
        
        value['Ports'] = ports
        params['result'] = {'returncode': True, 'value': value}
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
    #Just return False since the pointers are no longer supported.
    #The tasklet is not removed because pointers support will be reimplemented, so we will need 
    #to go back to this tasklet someday
    return False
#    return params['devicetype'] == "racktivity"

