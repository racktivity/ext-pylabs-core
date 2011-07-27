__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    port = None
    for p in meteringdevice.ports:
        if p.label == params['label']:
            port = p
            break
    if not port:
        events.raiseError("No port found with label '%s'" % params['label'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0054', tags='', escalate=False)

    #Delete the port from the meteringdevice and save to drp
    meteringdevice.ports.remove(port)
    p.api.model.racktivity.meteringdevice.save(meteringdevice)

    params['result'] = {'returncode':True}


def match(q, i, params, tags):
    return True