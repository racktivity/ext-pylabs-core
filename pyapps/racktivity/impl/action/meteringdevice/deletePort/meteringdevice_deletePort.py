__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'deletePort'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    port = None
    for p in meteringdevice.ports:
        if p.label == params['label']:
            port = p
            break
    if not port:
        events.raiseError("No port found with label '%s'" % params['label'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0054', tags='', escalate=False)

    #Delete the port from the meteringdevice and save to drp
    meteringdevice.ports.remove(port)
    q.drp.meteringdevice.save(meteringdevice)

    params['result'] = {'returncode':True}
    
    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True