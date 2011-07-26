__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    requiredsensor = None
    changed = False

    for sensor in meteringdevice.sensors:
        if sensor.label == params['sensorlabel']:
            requiredsensor = sensor
        elif sensor.label == params['newsensorlabel']:
            events.raiseError('Label must be unique within the module', messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0071', tags='', escalate=False)
        elif sensor.sequence == params['sequence']:
            events.raiseError('Sequence must be unique within the module', messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0072', tags='', escalate=False)
        

    if not requiredsensor:
        events.raiseError('Could not find sensor with label "%s" in module "%s"' % (params['sensorlabel'], meteringdevice.name), messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0073', tags='', escalate=False)

    fields = {'label': 'newsensorlabel', 'sequence': 'sequence', 'sensortype': 'sensortype', 'thresholdguids': 'thresholds', 'attributes': 'attributes'}
    for fieldkey, fieldvalue in fields.iteritems():
        if fieldvalue in params and params[fieldvalue]:
            if fieldkey == 'attributes':
                requiredsensor.attributes.update(params[fieldvalue])
            else:
                setattr(requiredsensor, fieldkey, params[fieldvalue])
            changed = True
    if changed:
        p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode':True}


def match(q, i, params, tags):
    return True