__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_addSensor'


def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Energy Switch Sensor details')
    tab.addText('label', 'Sensor label', optional=False)
    types = dict([(k, k.capitalize()) for k in q.enumerators.sensorporttype._pm_enumeration_items.keys()])
    tab.addChoice('type', 'Sensor Type', values=types)
    tab.addInteger('sequence', 'Sensor Sequence', minValue=len(meteringdevice.sensors)+1)
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']

    cloudapi.meteringdevice.addSensor(meteringdeviceguid, label=tab.elements['label'].value,
                                              sensortype=str(q.enumerators.sensorporttype.getByName(tab.elements['type'].value)), 
                                              sequence=tab.elements['sequence'].value)

    q.gui.dialog.showMessageBox('Sensor "%s" is being added to the energy switch %s' % (tab.elements['label'].value, meteringdevice.name), "Add Sensor")

def match(q, i, p, params, tags):
    return True
