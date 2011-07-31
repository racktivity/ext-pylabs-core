__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    port = None
    for powerinput in meteringdevice.powerinputs:
        if powerinput.label == params['label']:
            port = powerinput
            break
    if not port:
        raise ValueError("No input port found with label '%s'" % params['label'])

    meteringdevice.powerinputs.remove(powerinput)
    p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}



def match(q, i, params, tags):
    return True
