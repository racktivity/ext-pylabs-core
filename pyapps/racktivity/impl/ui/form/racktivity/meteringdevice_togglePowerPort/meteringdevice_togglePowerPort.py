__tags__ = "wizard", "meteringdevice_togglePowerPort"
__author__ = "racktivity"

def main(q, i, p, params, tags):
    cloudApi = p.api.action.racktivity

    label = params['extra']['label']
    mcguid = params['extra']['meteringdeviceguid']

    status = cloudApi.meteringdevice.getPowerPortStatus(mcguid, label)['result']['status']
    onoff = "off" if status else "on"
    
    answer = q.gui.dialog.showMessageBox("Are you sure you want to turn %s port '%s'?" % (onoff, label), "Power On Port", msgboxButtons="YesNo",
                                msgboxIcon="Question", defaultButton="No")
    
    if answer.lower() == "yes":
        if status:
            cloudApi.meteringdevice.powerOffPowerPort(mcguid, label)
        else:
            cloudApi.meteringdevice.powerOnPowerPort(mcguid, label)

def match(q, i, p, params, tags):
    return True
