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
    else:
        events.raiseError("Can't find application with meteringdeviceguid '%s'" % master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0030', tags='', escalate=False)
    portid = None
    for port in meteringdevice.ports:
        if port.label == params['label']:
            portid = port.sequence
            break
        
    datatype = params['meteringtype'] #can be either signal_current or signal_voltage
    
    result = q.actions.actor.meteringdevice.getPortData(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport,  meteringdevice.id, portid, datatype)
              
    params['result'] = result['value'] 
    
  

def match(q, i, params, tags):
    return True

