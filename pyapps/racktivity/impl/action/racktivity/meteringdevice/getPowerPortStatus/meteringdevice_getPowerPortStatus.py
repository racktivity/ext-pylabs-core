__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
        
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = p.api.model.racktivity.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)

    from rootobjectaction_lib import rootobjectaction_find
    applications = rootobjectaction_find.application_find(meteringdeviceguid=master.guid, name='MeteringdeviceAPI')
    masteripaddress = None
    deviceapiport = 0
    if applications:
        application = p.api.model.racktivity.racktivity_application.get(applications[0])
        service = application.networkservices[0]
        ipaddress = p.api.model.racktivity.ipaddress.get(service.ipaddressguids[0])
        masteripaddress = ipaddress.address
        deviceapiport = service.ports[0].portnr
    else:
        events.raiseError("Can't find application with meteringdeviceguid '%s'" % master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0030', tags='', escalate=False)

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

