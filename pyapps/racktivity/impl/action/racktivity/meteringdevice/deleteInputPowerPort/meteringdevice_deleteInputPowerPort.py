__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'deleteInputPowerPort'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = q.drp.meteringdevice.get(params['meteringdeviceguid'])
    port = None
    for powerinput in meteringdevice.powerinputs:
        if powerinput.label == params['label']:
            port = powerinput
            break
    if not port:
        events.raiseError("No input port found with label '%s'" % params['label'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0074', tags='', escalate=False)

    meteringdevice.powerinputs.remove(powerinput)
    q.drp.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True}
    
    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True