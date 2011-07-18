__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'addThresholdOnSensor'
from rootobjectaction_lib import events

def getSensor(meteringdevice, label):
    for sensor in meteringdevice.sensors:
        if sensor.label == label:
            return sensor

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = q.drp.meteringdevice.get(params['meteringdeviceguid'])
    label = params['sensorlabel']
    thresholdguid = params['thresholdguid']
    sensor = getSensor(meteringdevice, label)
    if not sensor:
        events.raiseError("Could not find sensor with label %s" % label, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0039', tags='', escalate=False)

    sensor.thresholdguids.append(thresholdguid)
    q.drp.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True