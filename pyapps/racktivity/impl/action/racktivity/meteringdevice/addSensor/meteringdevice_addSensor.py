__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
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
    
    p.api.model.racktivity.meteringdevice.save(meteringdevice)


    #Create a database for the sensor temperature (meteringdeviceguid_sensorid_temperature)
    sensorsequence = sensor.sequence
    
    sensordbname = str(sensor.sensortype).replace("SENSOR", "").lower()
    storename = '%s_%s_%s' % (meteringdeviceguid, sensorsequence, sensordbname)
    p.api.actor.graphdatabase.createStore(storename)

    params['result'] = {'returncode':True}


def match(q, i, params, tags):
    return True