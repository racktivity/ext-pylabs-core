__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    output = None
    for poweroutput in meteringdevice.poweroutputs:
        if poweroutput.label == params['portlabel']:
            output = poweroutput
            break
    
    if not output:
        events.raiseError("Can't find output port with label '%s'" % params['portlabel'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0050', tags='', escalate=False)
    
    output.cableguid = params['cableguid']
    p.api.model.racktivity.meteringdevice.save(meteringdevice)
    
    params['result'] = {'returncode':True}


def match(q, i, params, tags):
    return True