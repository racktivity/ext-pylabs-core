__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getCurrentSensorData'
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

    sensorid = None
    for sensor in meteringdevice.sensors:
        if sensor.label == params['label']:
            sensorid = sensor.sequence
            break
        
    result = q.actions.actor.meteringdevice.getSensorData(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id, sensorid, params['meteringtype'], master.accounts[0].login, master.accounts[0].password)
    params['result'] = {'returncode': True,
                        'value': result['value']}

def match(q, i, params, tags):
    return True

