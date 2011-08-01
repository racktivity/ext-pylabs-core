__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_addInputPowerPort'


def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Energy Switch Input Power Port details')
    tab.addText('label', 'Port label', optional=False)
    tab.addInteger('sequence', 'Port Sequence', minValue=len(meteringdevice.powerinputs)+1)
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']

    cloudapi.meteringdevice.addInputPowerPort(meteringdeviceguid, label=tab.elements['label'].value, sequence=tab.elements['sequence'].value)

    q.gui.dialog.showMessageBox('Input Power Port "%s" is being added to the energy switch %s' % (tab.elements['label'].value, meteringdevice.name), "Add Input Power Port")

def match(q, i, p, params, tags):
    return True
