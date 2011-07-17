__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getSignal'
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
    else:
        events.raiseError("Can't find racktivity_application with meteringdeviceguid '%s'" % master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0030', tags='', escalate=False)
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

