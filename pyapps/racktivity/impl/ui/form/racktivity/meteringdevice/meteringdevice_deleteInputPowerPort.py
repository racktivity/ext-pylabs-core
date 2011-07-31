__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_deleteInputPowerPort'


def main(q, i, params, tags):
    cloudapi = i.config.cloudApiConnection.find('main')
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Energy Switch Input Power Ports')
    powerinputs = list()
    for powerinput in meteringdevice.powerinputs:
        if not powerinput.cableguid:
            powerinputs.append(powerinput)
    if powerinputs:
        ports = dict([(k.sequence, k.label) for k in powerinputs])
        tab.addChoice('port', 'Select port to delete', values=ports)
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['main']
        cloudapi.meteringdevice.deleteInputPowerPort(meteringdeviceguid, label=ports[tab.elements['port'].value])
        q.gui.dialog.showMessageBox('Input Power Port "%s" is being deleted from the energy switch %s' % (ports[tab.elements['port'].value], meteringdevice.name),
                                    "Delete Input Power Port")
        return
    else:
        q.gui.dialog.showMessageBox('No disconnected Input Power Ports found for the energy switch %s' % (meteringdevice.name),
                                    "Delete Input Power Port")
    

def match(q, i, params, tags):
    return True
