__author__ = 'racktivity'
from rootobjectaction_lib import events

def getPowerPort(meteringdevice, label):
    returnvalue = None
    for powerport in meteringdevice.poweroutputs:
        if powerport.label == label:
            returnvalue = powerport
            break
    return returnvalue

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    label = params['powerportlabel']
    powerport = getPowerPort(meteringdevice, label)
    if not powerport:
        events.raiseError("Could not find powerport with label %s" % label, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0053', tags='', escalate=False)

    params['result'] = {'returncode': True,
                        'thresholdguid': powerport.thresholdguids}

def match(q, i, params, tags):
    return True