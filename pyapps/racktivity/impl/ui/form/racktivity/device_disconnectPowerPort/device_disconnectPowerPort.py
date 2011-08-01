__tags__ = "wizard", "device_disconnectPowerPort"
__author__ = "racktivity"

def main(q, i, p, params, tags):
    cloudApi = p.api.action.racktivity

    deviceguid = params['extra']['deviceguid']
    form = q.gui.form.createForm()
    tab = form.addTab("tab1", "General")
    device = cloudApi.device.getObject(deviceguid)
    powerportsdata = dict( (p.name, p) for p in device.powerports if p.cableguid)
    
    tab.message("msg","Provide information for the poweroutput to disconnect")
    
    tab.addDropDown("powerport", "Select device port", dict((x,x) for x in powerportsdata.iterkeys()))
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['tab1']
    powerport = powerportsdata[tab.elements['powerport'].value]
    cableguid = powerport.cableguid
    cloudApi.device.disconnectPowerPort(device.guid, powerport.name)
    q.gui.dialog.showMessageBox("Poweroutputport %s has been disconnected" % (powerport.name), "Disconnect PowerOutpurtPort")

def main(q, i, p, params, tags):
    return True