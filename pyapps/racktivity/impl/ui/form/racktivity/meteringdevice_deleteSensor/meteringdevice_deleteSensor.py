__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_deleteSensor'


def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Energy Switch Sensors')
    sensors = dict([(k.sequence, k.label) for k in meteringdevice.sensors])
    tab.addChoice('sensor', 'Select sensor to delete', values=sensors)
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']

    cloudapi.meteringdevice.deleteSensor(meteringdeviceguid, label=sensors[tab.elements['sensor'].value])

    q.gui.dialog.showMessageBox('Sensor "%s" is being deleted from the energy switch %s' % (sensors[tab.elements['sensor'].value], meteringdevice.name), "Delete Sensor")

def match(q, i, p, params, tags):
    return True
