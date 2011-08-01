__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    changed = False
    requiredpowerinput = None

    for powerinput in meteringdevice.powerinputs:
        if powerinput.label == params['portlabel']:
            requiredpowerinput = powerinput
        elif powerinput.label == params['newportlabel']:
            raise ValueError('Label must be unique within the module')
        elif powerinput.sequence == params['sequence']:
            raise ValueError('Sequence must be unique whithin the module')
    
    if not requiredpowerinput:
        raise ValueError('Could not find a power output port with label "%s" in module "%s"' % (params['portlabel'], meteringdevice.name))

    fields = {'label': 'newportlabel', 'sequence': 'sequence', 'attributes': 'attributes'}
    for fieldkey, fieldvalue in fields.iteritems():
        if fieldvalue in params and params[fieldvalue]:
            if fieldkey == 'attributes':
                requiredpowerinput.attributes.update(params[fieldvalue])
            else:
                setattr(requiredpowerinput, fieldkey, params[fieldvalue])
            changed = True
    if changed:
        p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode':True}



def match(q, i, params, tags):
    return True
