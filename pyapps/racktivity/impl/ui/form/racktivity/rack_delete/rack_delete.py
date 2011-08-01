__tags__ = "wizard", "rack_delete"
__author__ = "racktivity"

def main(q, i, p, params, tags):
    cloudApi = i.config.cloudApiConnection.find('main')

    rackguid = params['extra']['rackguid']
    
    devices = cloudApi.device.find(rackguid=rackguid)['result']['guidlist']
    meteringdevices = cloudApi.meteringdevice.find(rackguid=rackguid)['result']['guidlist']
    if devices or meteringdevices:
        num = len(devices) + len(meteringdevices)

        answer = q.gui.dialog.showMessageBox('''The current rack has %s connected device(s),
are you sure you want to delete this rack with 
all the connected device(s)?''' % num,
                                             "Delete rack", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
        if answer.lower() == "no":
            return
    rack = cloudApi.rack.getObject(rackguid)
    cloudApi.rack.delete(rackguid=rackguid)
    q.gui.dialog.showMessageBox("Rack '%s' is being deleted" % rack.name, "Delete rack")

def main(q, i, p, params, tags):
    return True