__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'setFixedIPAddress'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    changed = False
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = q.drp.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)
    from rootobjectaction_lib import rootobjectaction_find
    applicationguids = rootobjectaction_find.racktivity_application_find(meteringdeviceguid=master.guid, name='MeteringdeviceAPI')
    masteripaddress = None
    deviceapiport = 0
    if applications:
        racktivity_application = q.drp.racktivity_application.get(applications[0])
        services = racktivity_application.networkservices
        if services:
            service = services[0]
            ipaddress = q.drp.ipaddress.get(service.ipaddressguids[0])
            masteripaddress = ipaddress.address
            masternetworkport = service.ports[0]
            deviceapiport = masternetworkport.portnr
            ipaddress.address = params['ipaddress']
            ipaddress.netmask = params['subnetmask']
            lan = q.drp.lan.get(ipaddress.languid)
            lan.gateway = params['defaultgateway']
            changed = True
    else:
        events.raiseError("Can't find racktivity_application with meteringdeviceguid '%s'" % master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0030', tags='', escalate=False)
    if changed:
        q.drp.meteringdevice.save(meteringdevice)
    q.actions.actor.meteringdevice.setConfigurationParameter(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id, 'ipaddress', params['ipaddress'])
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True