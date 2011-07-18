__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'addThresholdOnPowerPort'
from rootobjectaction_lib import events

def getPowerPort(meteringdevice, label):
    for powerport in meteringdevice.poweroutputs:
        if powerport.label == label:
            return powerport

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = q.drp.meteringdevice.get(params['meteringdeviceguid'])
    label = params['powerportlabel']
    thresholdguid = params['thresholdguid']
    powerport = getPowerPort(meteringdevice, label)
    if not powerport:
        events.raiseError("Could not find powerport with label %s" % label, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0043', tags='', escalate=False)

    powerport.thresholdguids.append(thresholdguid)
    q.drp.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True