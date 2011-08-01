__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_addOutputPowerPort'


def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Energy Switch Output Power Port details')
    tab.addText('label', 'Port label', optional=False)
    tab.addInteger('sequence', 'Port Sequence', minValue=len(meteringdevice.poweroutputs)+1)
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']

    cloudapi.meteringdevice.addOutputPowerPort(meteringdeviceguid, label=tab.elements['label'].value, sequence=tab.elements['sequence'].value)

    q.gui.dialog.showMessageBox('Output Power Port "%s" is being added to the energy switch %s' % (tab.elements['label'].value, meteringdevice.name), "Add Output Power Port")

def match(q, i, p, params, tags):
    return True
