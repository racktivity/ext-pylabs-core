__author__ = 'racktivity'
__tags__ = 'wizard', 'meteringdevice_setStartupDelay'

def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    portlabel = params['extra']['portlabel']
    meteringdeviceguid = params['extra']['meteringdeviceguid']

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Set startup delay')
    tab.addInteger('delayValue', 'Startup delay for the selected power port', optional=False)

    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']
    delayvalue = tab.elements['delayValue'].value

    cloudapi.meteringdevice.setPowerPortStartupDelay(meteringdeviceguid, portlabel, delayvalue)
    q.gui.dialog.showMessageBox('Startup delay has been set to %s on the device'%delayvalue, "Set startup delay")

def match(q, i, p, params, tags):
    return True
