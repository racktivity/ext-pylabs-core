__tags__ = "wizard", "meteringdevice_disconnectPowerOutputPort"
__author__ = "racktivity"

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

def main(q, i, p, params, tags):
    cloudApi = p.api.action.racktivity

    meteringdeviceguid = params['extra']['meteringdeviceguid']
    outputports = getOuptuPorts(cloudApi, meteringdeviceguid)
    
    form = q.gui.form.createForm()
    tab = form.addTab("tab1", "General")
    meteringdevice = cloudApi.meteringdevice.getObject(meteringdeviceguid)
    poweroutports = dict((i, p['label']) for i, p in enumerate(outputports) if p['cableguid'])
    #powerportsdata = dict( (p.label, p) for p in meteringdevice.poweroutputs if p.cableguid)
    
    tab.message("msg","Provide information for the poweroutput to disconnect")
    
    tab.addDropDown("powerport", "Select energy switch port", poweroutports)
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['tab1']
    powerport = outputports[int(tab.elements['powerport'].value)]
    cloudApi.meteringdevice.disconnectPowerOutputPort(powerport['mdguid'], powerport['label'])
    q.gui.dialog.showMessageBox("Poweroutputport %s has been disconnected" % (powerport['label']), "Disconnect PowerOutpurtPort")

def main(q, i, p, params, tags):
    return True