__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getJSON'

def main(q, i, params, tags):
    import json
    info = dict()
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = q.drp.meteringdevice.get(meteringdeviceguid)
    fields=['name', 'id', 'parentmeteringdeviceguid', 'rackguid', 'clouduserguid', 'positionx', 'positionz', 'tags']
    for field in fields:
        info[field] = getattr(meteringdevice, field, None)
    info['meteringdevicetype'] =  str(meteringdevice.meteringdevicetype)
    info['attributes'] = meteringdevice.attributes._dict if meteringdevice.attributes._dict else None 
    info['meteringdeviceconfigstatus'] = str(meteringdevice.meteringdeviceconfigstatus)
    powerinputs = []
    poweroutputs = []
    sensors = []
    ports = []
    accounts = []
    for powerinput in meteringdevice.powerinputs:
        powerinputs.append({'label': powerinput.label, 'sequence': powerinput.sequence, 'cableguid': powerinput.cableguid, 'attributes': powerinput.attributes if powerinput.attributes else None})
    for poweroutput in meteringdevice.poweroutputs:
        poweroutputs.append({'label': poweroutput.label, 'sequence': poweroutput.sequence, 'cableguid': poweroutput.cableguid, 'attributes': poweroutput.attributes if poweroutput.attributes else None})
    info['powerinputs'] = powerinputs
    info['poweroutputs'] = poweroutputs
    for sensor in meteringdevice.sensors:
        sensors.append({'label': sensor.label, 'sequence': sensor.sequence, 'sensortype': str(sensor.sensortype), 'attributes': sensor.attributes if sensor.attributes else None})
    info['sensors'] = sensors
    for port in meteringdevice.ports:
        ports.append({'label': port.label, 'sequence': port.sequence, 'porttype': str(port.porttype), 'attributes': port.attributes if port.attributes else None})
    info['ports'] = ports
    for account in meteringdevice.accounts:
        accounts.append({'login': account.login, 'password': account.password})
    info['accounts'] = accounts

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
        if service.ipaddressguids:
            ipaddress = q.drp.ipaddress.get(service.ipaddressguids[0])
            masteripaddress = ipaddress.address
        else:
            masteripaddress = None
    info['ipaddress'] = masteripaddress

    params['result'] = json.dumps(info)

def match(q, i, params, tags):
    return True
