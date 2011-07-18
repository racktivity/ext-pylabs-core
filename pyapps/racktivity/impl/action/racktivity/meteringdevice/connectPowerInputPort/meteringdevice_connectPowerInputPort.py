__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'connectPowerInputPort'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    input = None
    for powerinput in meteringdevice.powerinputs:
        if powerinput.label == params['portlabel']:
            input = powerinput
            break
    
    if not input:
        events.raiseError("Can't find input port with label '%s'" % params['portlabel'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0047', tags='', escalate=False)
    
    input.cableguid = params['cableguid']
    q.drp.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}
    
    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True