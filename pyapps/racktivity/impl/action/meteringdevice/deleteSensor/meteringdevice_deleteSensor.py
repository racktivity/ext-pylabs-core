__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'deleteSensor'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    sensor = None
    for s in meteringdevice.sensors:
        if s.label == params['label']:
            sensor = s
            break
    if not sensor:
        events.raiseError("No sensor found with label '%s'" % params['label'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0069', tags='', escalate=False)

    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name
    
    sensordbname = str(sensor.sensortype).replace("SENSOR", "").lower()
    databasenames = ('%s_%s_%s' % (meteringdeviceguid, sensor.sequence, sensordbname), )
        
    q.actions.actor.graphdatabase.destroyStores(url, databasenames)

    meteringdevice.sensors.remove(sensor)
    q.drp.meteringdevice.save(meteringdevice)

    params['result'] = {'returncode':True}
    
    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True