__author__ = 'aserver'
__priority__= 3
from rootobjectaction_lib import events

def getPort(ports, seq):
    for port in ports:
        if port["sequence"] == seq:
            return port
    return False

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False, "data" :list()}
    guid = params["rootobjectguid"]
    portlabel = params["portlabel"] 
    meteringUnits = {"Voltage":"V", "Power":"W", "Current":"A", "PowerFactor":"", "ActiveEnergy":"kwh"}
    from rootobjectaction_lib import rootobjectaction_find
    ca = i.config.cloudApiConnection.find("main")
    #get port sequence
    md = ca.meteringdevice.getObject(guid)

    devData = ca.meteringdevice.getCurrentDeviceData(guid, "all")['result']['value']
    data = dict()
    
    #if portlabel and params["sensorlabel"]:
    #    raise ValueError("You can not specify both sensorlabel and portlabel")
    if portlabel:
        portseq = -1
        for port in md.poweroutputs:
            if port.label == portlabel:
                portseq = port.sequence
                break
            if portseq < 0:
                raise ValueError("Port label was not found")

        port = getPort(devData["Ports"], portseq)
        port["Voltage"] = devData["Voltage"]
        for key in port:
            if key in meteringUnits:
                params['result']["data"].append({"viewdatatype":key,"viewdatavalue":port[key], "viewdataunit":meteringUnits[key]})
    #elif params["sensorlabel"] :
    #    raise NotImplementedError("Getting sensor data from emulator is not implemented yet")
    else:
        data["Current"] = devData["TotalCurrent"]
        data["Power"] = devData["TotalPower"]
        data["PowerFactor"] = devData["TotalPowerFactor"]
        data["ActiveEnergy"] = devData["TotalActiveEnergy"]
        data["Voltage"] = devData["Voltage"]
        for key in data:
            params['result']["data"].append({"viewdatatype":key,"viewdatavalue":data[key], "viewdataunit":meteringUnits[key]})

def match(q, i, params, tags):
    return True
