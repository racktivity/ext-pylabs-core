__tags__ = "wizard", "device_delete"
__author__ = "racktivity"

def deleteDevice(q, deviceguid, cloudApi, ask=True):
    powerports = cloudApi.device.listPowerPorts(deviceguid=deviceguid)['result']['powerports']
    if powerports:
        num = 0
        for powerport in powerports:
            if powerport["status"] == str(q.enumerators.powerportstatustype.ACTIVE):
                num += 1
        if ask:
            answer = q.gui.dialog.showMessageBox('''The current device has %s active powerport(s). 
Are you sure you want to delete this device?''' % num,\
                                                    "Delete device", msgboxButtons="YesNo",
                                                    msgboxIcon="Question", defaultButton="No")
            if answer == "No":
                return False
    cloudApi.device.delete(deviceguid=deviceguid)
    return True

def main(q, i, p, params, tags):
    cloudApi = p.api.action.racktivity
    deviceguid = params['extra']['deviceguid']
    device = cloudApi.device.getObject(deviceguid)
    if deleteDevice(q, deviceguid, cloudApi):
        q.gui.dialog.showMessageBox("device '%s' is being deleted" % device.name, "Delete device")

def match(q, i, p, params, tags):
    return True
