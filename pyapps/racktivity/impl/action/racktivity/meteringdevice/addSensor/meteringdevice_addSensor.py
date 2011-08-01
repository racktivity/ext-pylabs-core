__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    for sensor in meteringdevice.sensors:
        if sensor.label == params['label']:
            raise ValueError('Sensor label must be unique within the module')

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
        raise ValueError("Sequence must be 1 or more")
    
    #validate the sequence and the label
    for s in meteringdevice.sensors:
        if sensor.sequence == s.sequence:
            raise ValueError("Sequence '%s' is already taken by another sensor" % sensor.sequence)
        
    meteringdevice.sensors.append(sensor)
    
    p.api.model.racktivity.meteringdevice.save(meteringdevice)


    #Create a database for the sensor temperature (meteringdeviceguid_sensorid_temperature)
    sensorsequence = sensor.sequence
    
    sensordbname = str(sensor.sensortype).replace("SENSOR", "").lower()
    storename = '%s_%s_%s' % (meteringdeviceguid, sensorsequence, sensordbname)
    p.api.actor.racktivity.graphdatabase.createStore(storename)

    params['result'] = {'returncode':True}


def match(q, i, params, tags):
    return True
