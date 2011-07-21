__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    input = None
    for powerinput in meteringdevice.powerinputs:
        if powerinput.label == params['portlabel']:
            input = powerinput
            break
    
    if not input:
        events.raiseError("Can't find input port with label '%s'" % params['portlabel'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0047', tags='', escalate=False)
    
    input.cableguid = params['cableguid']
    p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}
    
    #import racktivityui.uigenerator.meteringdevice
    #racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True