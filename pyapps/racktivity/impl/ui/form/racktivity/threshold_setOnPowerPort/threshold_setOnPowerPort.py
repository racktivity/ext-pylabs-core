__author__ = 'racktivity'
__tags__ = 'wizard', 'threshold_setOnPowerPort'

def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    portlabel = params['extra']['portlabel']
    meteringdeviceguid = params['extra']['meteringdeviceguid']

    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Set Threshold')
    
    thresholddict = {'MaxCurrentOff': 'Maximum Current Off',
                     'MaxCurrentWarning':'Maximum Current Warning',
                     'MaxPowerOff': 'Maximum Power Off',
                     'MaxPowerWarning': 'Maximum Power Warning'}
    
    tab.addChoice('thresholdtype', 'Select Threshold to set', thresholddict, optional=False)
    tab.addInteger('thresholdvalue', 'Threshold value to set', optional=False)

    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']
    thresholdtype = tab.elements['thresholdtype'].value
    thresholdvalue = tab.elements['thresholdvalue'].value

    cloudapi.meteringdevice.setThresholdOnPowerPort(meteringdeviceguid, portlabel, thresholdtype, thresholdvalue)
    q.gui.dialog.showMessageBox('Threshold is being set on the device', "Create Threshold")

def match(q, i, p, params, tags):
    return True
