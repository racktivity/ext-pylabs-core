__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_deleteOutputPowerPort'


def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    portlabel = None
    if params['extra'].has_key('portlabel'):
        portlabel = params['extra']['portlabel']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)
    if portlabel:
        cloudapi.meteringdevice.deleteOutputPowerPort(meteringdeviceguid, portlabel)
        q.gui.dialog.showMessageBox('Output Power Port "%s" is being deleted from the energy switch %s' % (portlabel, meteringdevice.name),
                                 "Delete Output Power Port")
        return
    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Energy Switch Output Power Ports')
    poweroutputs = list()
    for poweroutput in meteringdevice.poweroutputs:
        if not poweroutput.cableguid:
            poweroutputs.append(poweroutput)
    if poweroutputs:
        ports = dict([(k.sequence, k.label) for k in poweroutputs])
        tab.addChoice('port', 'Select port to delete', values=ports)
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        cloudapi.meteringdevice.deleteOutputPowerPort(meteringdeviceguid, label=ports[tab.elements['port'].value])
        q.gui.dialog.showMessageBox('Output Power Port "%s" is being deleted from the energy switch %s' % (ports[tab.elements['port'].value], meteringdevice.name),
                                    "Delete Output Power Port")
        return
    else:
        q.gui.dialog.showMessageBox('No disconnected Output Power Ports found for the energy switch %s' % (meteringdevice.name),
                                    "Delete Output Power Port")
    

def main(q, i, p, params, tags):
    return True
