__author__ = 'racktivity'
__tags__ = 'wizard', 'threshold_setOnDevice'

def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    meteringdeviceguid = params['extra']['meteringdeviceguid']
    
    form = q.gui.form.createForm()
    tab = form.addTab('main', 'Set Threshold')
    
    thresholddict = {'MaxTotalCurrentOff': 'Maximum Total Current Off', 'MaxTotalCurrentWarning': 'Maximum Total Current Warning',
                     'MaxTotalPowerOff': 'Maximum Total Power Off', 'MaxTotalPowerWarning': 'Maximum Total Power Warning',
                     'MaxVoltageOff': 'Maximum Voltage Off', 'MaxVoltageWarning': 'Maximum Voltage Warning', 'MinVoltageOff': 'Minimum Voltage Off',
                     'MinVoltageWarning': 'Minimum Voltage Warning'}
    
    tab.addChoice('thresholdtype', 'Select Threshold to set', thresholddict, optional=False)
    tab.addInteger('thresholdvalue', 'Threshold value to set', optional=False)

    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['main']
    thresholdtype = tab.elements['thresholdtype'].value
    thresholdvalue = tab.elements['thresholdvalue'].value

    cloudapi.meteringdevice.setThreshold(meteringdeviceguid, thresholdtype, thresholdvalue)
    q.gui.dialog.showMessageBox('Threshold is being set on the device', "Create Threshold")

def main(q, i, p, params, tags):
    return True
