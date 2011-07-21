__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    changed = False
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = p.api.model.racktivity.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)
    from rootobjectaction_lib import rootobjectaction_find
    applicationguids = rootobjectaction_find.application_find(meteringdeviceguid=master.guid, name='MeteringdeviceAPI')
    masteripaddress = None
    deviceapiport = 0
    if applications:
        application = p.api.model.racktivity.racktivity_application.get(applications[0])
        services = application.networkservices
        if services:
            service = services[0]
            ipaddress = p.api.model.racktivity.ipaddress.get(service.ipaddressguids[0])
            masteripaddress = ipaddress.address
            masternetworkport = service.ports[0]
            deviceapiport = masternetworkport.portnr
            ipaddress.address = params['ipaddress']
            ipaddress.netmask = params['subnetmask']
            lan = p.api.model.racktivity.lan.get(ipaddress.languid)
            lan.gateway = params['defaultgateway']
            changed = True
    else:
        events.raiseError("Can't find application with meteringdeviceguid '%s'" % master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0030', tags='', escalate=False)
    if changed:
        p.api.model.racktivity.meteringdevice.save(meteringdevice)
    q.actions.actor.meteringdevice.setConfigurationParameter(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id, 'ipaddress', params['ipaddress'])
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True