__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'addSensor'
from rootobjectaction_lib import events

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    for sensor in meteringdevice.sensors:
        if sensor.label == params['label']:
            events.raiseError('Sensor label must be unique within the module', messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0060', tags='', escalate=False)

    fields = ('label', 'sensortype', 'sequence')
    sensor = meteringdevice.sensors.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(sensor, key, value)
    
    if not sensor.sequence:
        maxsequence = 0
        for s in meteringdevice.sensors:
            maxsequence = max(s.sequence, maxsequence)
        sensor.sequence = maxsequence + 1
    
    if sensor.sequence <= 0:
        events.raiseError("Sequence must be 1 or more", messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0061', tags='', escalate=False)
    
    #validate the sequence and the label
    for s in meteringdevice.sensors:
        if sensor.sequence == s.sequence:
            events.raiseError("Sequence '%s' is already taken by another sensor" % sensor.sequence, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0062', tags='', escalate=False)
        
    meteringdevice.sensors.append(sensor)
    
    q.drp.meteringdevice.save(meteringdevice)

    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name


    #Create a database for the sensor temperature (meteringdeviceguid_sensorid_temperature)
    sensorsequence = sensor.sequence
    
    sensordbname = str(sensor.sensortype).replace("SENSOR", "").lower()
    storename = '%s_%s_%s' % (meteringdeviceguid, sensorsequence, sensordbname)
    q.actions.actor.graphdatabase.createStore(url, storename)

    params['result'] = {'returncode':True}
    
    import racktivityui.uigenerator.meteringdevice
    racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)

def match(q, i, params, tags):
    return True