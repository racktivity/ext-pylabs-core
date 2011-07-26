from pymonkey import q, i
from cloud_api_client.Exceptions import CloudApiException

def create(name, id, rackguid,
           parentmeteringdeviceguid=None,
           login='root',
           password='rooter',
           meteringdevicetype='racktivity',
           ipaddressguid=None,
           port=0,
           powerinputsnumber=0,
           poweroutputsnumber=0,
           sensorsnumber=0,
           tags = None):
    
    cloudapi = i.config.cloudApiConnection.find('main')
    
    inputs = list()
    for index in range(powerinputsnumber):
        seq = index+1
        inputs.append({'sequence': seq,
                      'label': 'input-%s' % seq})
    
    ports= list()
    for index in range(poweroutputsnumber):
        seq = index+1
        ports.append({'sequence': seq,
                      'label': 'output-%s' % seq})
    
    sensors = list()
    for index in range(sensorsnumber):
        seq = index + 1
        sensors.append({'sequence': seq,
                        'label': 'sensor-%s' % seq})
    
    nics = list()
    if ipaddressguid:
        nics.append({'ipaddressguids':[ipaddressguid], 'status': str(q.enumerators.nicstatustype.ACTIVE),
                     'nictype': str(q.enumerators.nictype.ETHERNET_GB), 'order':0})
        
    attributes = {'deviceapiportnr': str(port)} if port else {}
    guid = cloudapi.meteringdevice.create(name=name, id=id, meteringdevicetype=meteringdevicetype, template=False, rackguid=rackguid,
                                          parentmeteringdeviceguid=parentmeteringdeviceguid,
                                          powerinputinfo=inputs,
                                          poweroutputinfo=ports,
                                          sensorinfo=sensors,
                                          nicinfo=nics,
                                          accounts=[{'login': login, 'password': password}],
                                          attributes=attributes,
                                          tags = tags)['result']['meteringdeviceguid']
    device = cloudapi.meteringdevice.getObject(guid)
    if device.name != name:
        raise RuntimeError("Device wasn't created probably '%s'" % guid)
    return guid

def createRacktivity(name, rackguid, login='root', password='rooter', ipaddressguid=None, port=6543, meteringdevicetype='racktivity'):
    masterguid = create(name, 'M1', rackguid, login=login, password=password, ipaddressguid=ipaddressguid, port=port, meteringdevicetype=meteringdevicetype)
    powermoduleguid = create("%s-power" % name, 'P1', rackguid, parentmeteringdeviceguid=masterguid, poweroutputsnumber=8,meteringdevicetype=meteringdevicetype)
    return masterguid, powermoduleguid

def delete(guid):
    cloudapi = i.config.cloudApiConnection.find('main')
    cloudapi.meteringdevice.delete(guid)
    try:
        devices = cloudapi.meteringdevice.getObject(guid)
        raise RuntimeError("Meteringdevice '%s' didn't delete probably" % guid)
    except CloudApiException:
        pass #success
        