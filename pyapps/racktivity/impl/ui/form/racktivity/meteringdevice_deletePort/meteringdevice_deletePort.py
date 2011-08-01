__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_deletePort'


def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    meteringdevice = cloudapi.meteringdevice.getObject(meteringdeviceguid)

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Energy Switch Ports')
    ports = dict([(k.sequence, k.label) for k in meteringdevice.ports])
    tab.addChoice('port', 'Select port to delete', values=ports)
    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']

    cloudapi.meteringdevice.deletePort(meteringdeviceguid, label=ports[tab.elements['port'].value])

    q.gui.dialog.showMessageBox('Port "%s" is being deleted from the energy switch %s' % (ports[tab.elements['port'].value], meteringdevice.name), "Delete Port")

def match(q, i, p, params, tags):
    return True
