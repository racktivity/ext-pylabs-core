__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    port = None
    for pt in meteringdevice.ports:
        if pt.label == params['label']:
            port = pt
            break
    if not port:
        raise ValueError("No port found with label '%s'" % params['label'])

    #Delete the port from the meteringdevice and save to drp
    meteringdevice.ports.remove(port)
    p.api.model.racktivity.meteringdevice.save(meteringdevice)

    params['result'] = {'returncode':True}


def match(q, i, params, tags):
    return True
