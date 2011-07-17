__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'listThresholdsOnSensor'
from rootobjectaction_lib import events

def getSensor(meteringdevice, label):
    toreturn = None
    for sensor in meteringdevice.sensors:
        if sensor.label == label:
            toreturn = sensor
            break
    return toreturn

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = q.drp.meteringdevice.get(params['meteringdeviceguid'])
    label = params['sensorlabel']
    sensor = getSensor(meteringdevice, label)
    if not sensor:
        events.raiseError("Could not find powerport with label %s" % label, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0053', tags='', escalate=False)
    
    params['result'] = {'returncode': True,
                        'thresholdguid': sensor.thresholdguids}

def match(q, i, params, tags):
    return True