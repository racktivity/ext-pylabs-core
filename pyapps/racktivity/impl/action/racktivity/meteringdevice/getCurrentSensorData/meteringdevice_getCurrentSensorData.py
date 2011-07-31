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

    sensorid = None
    for sensor in meteringdevice.sensors:
        if sensor.label == params['label']:
            sensorid = sensor.sequence
            break
        
    result = p.api.actor.racktivity.meteringdevice.getSensorData(meteringdeviceguid, master.meteringdevicetype, master.network.ipaddress, master.network.port, meteringdevice.id, sensorid, params['meteringtype'], master.accounts[0].login, master.accounts[0].password)
    params['result'] = {'returncode': True,
                        'value': result['value']}

def match(q, i, params, tags):
    return True
