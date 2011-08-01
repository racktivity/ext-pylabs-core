__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_updateOutputPowerPort'


def main(q, i, p, params, tags):
    cloudapi = i.config.cloudApiConnection.find('main')
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    portlabel = params['extra']['portlabel']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Energy Switch Output Power Port details')
    tab.addText('label', 'Port label', optional=False, value=portlabel)
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']
    newportlabel=tab.elements['label'].value
    if newportlabel != portlabel:
        cloudapi.meteringdevice.updatePowerOutputPort(meteringdeviceguid, portlabel, newportlabel=newportlabel)
        q.gui.dialog.showMessageBox('Output Power Port name is being updated to "%s"' % tab.elements['label'].value, "Update Output Power Port")

def main(q, i, p, params, tags):
    return True
