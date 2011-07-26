__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    sensor = None
    for s in meteringdevice.sensors:
        if s.label == params['label']:
            sensor = s
            break
    if not sensor:
        events.raiseError("No sensor found with label '%s'" % params['label'], messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0069', tags='', escalate=False)


    sensordbname = str(sensor.sensortype).replace("SENSOR", "").lower()
    databasenames = ('%s_%s_%s' % (meteringdeviceguid, sensor.sequence, sensordbname), )
        
    p.api.actor.graphdatabase.destroyStores(databasenames)

    meteringdevice.sensors.remove(sensor)
    p.api.model.racktivity.meteringdevice.save(meteringdevice)

    params['result'] = {'returncode':True}



def match(q, i, params, tags):
    return True