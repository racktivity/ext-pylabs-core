__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_addPort'


def main(q, i, params, tags):
    cloudapi = i.config.cloudApiConnection.find('main')
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Energy Switch Port details')
    tab.addText('label', 'Port label', optional=False)
    types = dict([(k, k.capitalize()) for k in q.enumerators.porttype._pm_enumeration_items.keys()])
    tab.addChoice('type', 'Port Type', values=types)
    tab.addInteger('sequence', 'Port Sequence', minValue=len(meteringdevice.ports)+1)
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']

    cloudapi.meteringdevice.addPort(meteringdeviceguid, label=tab.elements['label'].value,
                                                      porttype=str(q.enumerators.porttype.getByName(tab.elements['type'].value)),
                                                      sequence=tab.elements['sequence'].value)

    q.gui.dialog.showMessageBox('Port "%s" is being added to the energy switch %s' % (tab.elements['label'].value, meteringdevice.name), "Add Port")

def match(q, i, params, tags):
    return True
