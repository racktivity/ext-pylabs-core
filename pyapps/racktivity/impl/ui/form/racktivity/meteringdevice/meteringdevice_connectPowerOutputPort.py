__tags__ = "wizard", "meteringdevice_connectPowerOutputPort"
__author__ = "racktivity"

def callback_fill_ports(q, i, params, tags):
    form = q.gui.form.createForm()
    formData = params['formData']
    form.loadForm(formData)
    fill_ports(q, form, params)
    return form

def fill_ports(q, form, params):
    tab= form.tabs['tab1']
    deviceguid = tab.elements['device'].value
    if not deviceguid and tab.elements['device'].values:
        deviceguid = tab.elements['device'].values.keys()[0] 
    device = params['SESSIONSTATE']['devicesdata'].get(deviceguid)
    if not device: 
        return
    portsdata = dict ( (p.name, p) for p in device.powerports if p.status == q.enumerators.powerportstatustype.NOTCONNECTED)
    params['SESSIONSTATE']['powerportsdata'] = portsdata
    tab.elements['powerport'].values = dict((x,x) for x in portsdata.iterkeys())

def getOuptuPorts(cloudApi, mdguid):
    md = cloudApi.meteringdevice.getObject(mdguid)
    ports = list()
    for port in md.poweroutputs:
        p = {'mdguid': md.guid,
             'label': port.label,
             'sequence': port.sequence,
             'cableguid': port.cableguid}
        ports.append(p)
    children = cloudApi.meteringdevice.find(parentmeteringdeviceguid=md.guid)['result']['guidlist']
    for childguid in children:
        ports += getOuptuPorts(cloudApi, childguid)
    
    return ports

def main(q,i,params,tags):
    cloudApi = i.config.cloudApiConnection.find('main')

    meteringdeviceguid = params['extra']['meteringdeviceguid']
    form = q.gui.form.createForm()
    tab = form.addTab("tab1", "General")
    devicesdata = dict()
    params['SESSIONSTATE']['devicesdata'] = devicesdata
    outputports = getOuptuPorts(cloudApi, meteringdeviceguid)
    
    meteringdevice = cloudApi.meteringdevice.getObject(meteringdeviceguid)
    poweroutports = dict((i, p['label']) for i, p in enumerate(outputports) if not p['cableguid'])
    
    for deviceguid in cloudApi.device.find(rackguid=meteringdevice.rackguid)['result']['guidlist']:
            obj = cloudApi.device.getObject(deviceguid)
            devicesdata[obj.guid] = obj
    tab.message("msg1", "Provide information for the poweroutput to connect")
    
    tab.addDropDown("poweroutputport", "Select energy switch port", poweroutports)
    tab.addDropDown("device", "Select device ", dict((d.guid, d.name) for d in devicesdata.itervalues()), callback="fill_ports", trigger='change')
    tab.addDropDown("powerport", "Select port device port", dict())
    tab.addText("lbl", "Cable label")
    
    tab.addText("description", "Cable description", multiline=True)
    fill_ports(q, form, params)
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['tab1']
    deviceguid = tab.elements['device'].value
    device = params['SESSIONSTATE']['devicesdata'][deviceguid]
    label = tab.elements['lbl'].value
    poweroutputport = outputports[int(tab.elements['poweroutputport'].value)]
    description = tab.elements['description'].value
    cableguid = cloudApi.cable.create(label, str(q.enumerators.cabletype.POWERCABLE), description)['result']['cableguid']
    powerport = params['SESSIONSTATE']['powerportsdata'][str(tab.elements['powerport'].value)]
    cloudApi.device.connectPowerPort(deviceguid, powerport.name, cableguid)
    cloudApi.meteringdevice.connectPowerOutputPort(poweroutputport['mdguid'], poweroutputport['label'], cableguid)
    # Update the config status for the metering device to USED
    cloudApi.meteringdevice.updateModelProperties(meteringdeviceguid, meteringdeviceconfigstatus=str(q.enumerators.meteringdeviceconfigstatus.USED))
    q.gui.dialog.showMessageBox("Poweroutputport %s has been connected to device %s on powerport %s" % (poweroutputport['label'], device.name, powerport.name), "Connect PowerOutpurtPort")

def match(q,i,params,tags):
    return True