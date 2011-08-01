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
            raise ValueError('Label must be unique within the module')
        elif sensor.sequence == params['sequence']:
            raise ValueError('Sequence must be unique within the module')
        

    if not requiredsensor:
        raise ValueError('Could not find sensor with label "%s" in module "%s"' % (params['sensorlabel'], meteringdevice.name))

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
