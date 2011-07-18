__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getPowerPortStatus'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
        
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = q.drp.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)

    from rootobjectaction_lib import rootobjectaction_find
    applications = rootobjectaction_find.racktivity_application_find(meteringdeviceguid=master.guid, name='MeteringdeviceAPI')
    masteripaddress = None
    deviceapiport = 0
    if applications:
        racktivity_application = q.drp.racktivity_application.get(applications[0])
        service = racktivity_application.networkservices[0]
        ipaddress = q.drp.ipaddress.get(service.ipaddressguids[0])
        masteripaddress = ipaddress.address
        deviceapiport = service.ports[0].portnr
    else:
        events.raiseError("Can't find racktivity_application with meteringdeviceguid '%s'" % master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0030', tags='', escalate=False)

    portid = None
    for port in meteringdevice.poweroutputs:
        if port.label == params['portlabel']:
            portid = port.sequence
            break
    
    if portid == None:
        events.raiseError("Can't find port sequence for a port with label '%s'" % params['portlabel'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0052', tags='', escalate=False)

    actorresult = q.actions.actor.meteringdevice.getPowerPortStatus(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id, portid, master.accounts[0].login, master.accounts[0].password)['result']
    actorresult['text'] = "On" if actorresult['status'] else "Off"
    params['result'] = actorresult

def match(q, i, params, tags):
    return True

