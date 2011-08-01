__tags__ = "wizard", "device_connectPowerPort"
__author__ = "racktivity"

def callback_fill_ports(q, i, params, tags):
    form = q.gui.form.createForm()
    formData = params['formData']
    form.loadForm(formData)
    fill_ports(form, params)
    return form

def fill_ports(form, params):
    tab= form.tabs['tab1']
    device = params['SESSIONSTATE']['meteringdevicesdata'].get(tab.elements['meteringdevice'].value)
    if not device:
        return
    portsdata = dict ( (p.label, p) for p in device.poweroutputs if not p.cableguid)
    params['SESSIONSTATE']['meteringdeviceportsdata'] = portsdata
    tab.elements['meteringdeviceport'].values = dict((x,x) for x in portsdata.iterkeys())

def main(q, i, p, params, tags):
    cloudApi = i.config.cloudApiConnection.find('main')

    deviceguid = params['extra']['deviceguid']
    form = q.gui.form.createForm()
    tab = form.addTab("tab1", "General")
    meteringdevicesdata = dict()
    params['SESSIONSTATE']['meteringdevicesdata'] = meteringdevicesdata
    device = cloudApi.device.getObject(deviceguid)
    devportsdata = dict( (p.name, p) for p in device.powerports if p.status == q.enumerators.powerportstatustype.NOTCONNECTED)
    devports = dict((x,x) for x in devportsdata.keys())
    
    for meteringdeviceguid in cloudApi.meteringdevice.find(rackguid=device.rackguid)['result']['guidlist']:
        obj = cloudApi.meteringdevice.getObject(meteringdeviceguid)
        meteringdevicesdata[obj.guid] = obj
    tab.message("msg1", "Provide information for the poweroutput to connect")
    
    tab.addDropDown("deviceport", "Select device port", devports)
    tab.addDropDown("meteringdevice", "Select device ", dict((d.guid, d.name) for d in meteringdevicesdata.itervalues()), callback="fill_ports", trigger='change')
    tab.addDropDown("meteringdeviceport", "Select port device port", dict())
    fill_ports(form, params)
    tab.addText("lbl", "Cable label")
    
    tab.addText("description", "Cable description", multiline=True)
    
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['tab1']
    meteringdeviceguid = tab.elements['meteringdevice'].value
    meteringdevice = params['SESSIONSTATE']['meteringdevicesdata'][meteringdeviceguid]
    label = tab.elements['lbl'].value
    devport = devportsdata[tab.elements['deviceport'].value]
    description = tab.elements['description'].value
    cableguid = cloudApi.cable.create(label, str(q.enumerators.cabletype.POWERCABLE), description)['result']['cableguid']
    meteringdeviceport = params['SESSIONSTATE']['meteringdeviceportsdata'][tab.elements['meteringdeviceport'].value]
    cloudApi.meteringdevice.connectPowerOutputPort(meteringdeviceguid, meteringdeviceport.label, cableguid)
    cloudApi.device.connectPowerPort(deviceguid, devport.name, cableguid)
    q.gui.dialog.showMessageBox("Powerport %s has been connected to meteringdevice %s on powerport %s" % (devport.name, meteringdevice.name, meteringdeviceport.label), "Connect PowerOutpurtPort")

def main(q, i, p, params, tags):
    return True
