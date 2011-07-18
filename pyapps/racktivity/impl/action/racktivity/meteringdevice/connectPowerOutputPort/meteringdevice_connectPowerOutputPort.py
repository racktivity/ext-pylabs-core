__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'connectPowerOutputPort'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    output = None
    for poweroutput in meteringdevice.poweroutputs:
        if poweroutput.label == params['portlabel']:
            output = poweroutput
            break
    
    if not output:
        events.raiseError("Can't find output port with label '%s'" % params['portlabel'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0050', tags='', escalate=False)
    
    output.cableguid = params['cableguid']
    q.drp.meteringdevice.save(meteringdevice)
    
    params['result'] = {'returncode':True}
    
    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True