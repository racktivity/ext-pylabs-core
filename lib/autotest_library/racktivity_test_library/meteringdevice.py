from pylabs import i,q,p
from xmlrpclib import Fault

def create(name, id, rackguid,
           parentmeteringdeviceguid=None,
           login='root',
           password='rooter',
           meteringdevicetype='racktivity',
           ipaddress=None,
           port=0,
           powerinputsnumber=0,
           poweroutputsnumber=0,
           sensorsnumber=0,
           tags = None):
    
    cloudapi = p.api.action.racktivity
    
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
    
    networkinfo = None
    if ipaddress:
        networkinfo = {"ipaddress":ipaddress, "port":port, "protocol":"http"}
        
    guid = cloudapi.meteringdevice.create(name=name, id=id, meteringdevicetype=meteringdevicetype, template=False, rackguid=rackguid,
                                          parentmeteringdeviceguid=parentmeteringdeviceguid,
                                          powerinputinfo=inputs,
                                          poweroutputinfo=ports,
                                          sensorinfo=sensors,
                                          networkinfo=networkinfo,
                                          accounts=[{'login': login, 'password': password}],
                                          tags = tags)['result']['meteringdeviceguid']
    device = cloudapi.meteringdevice.getObject(guid)
    if device.name != name:
        raise RuntimeError("Device wasn't created probably '%s'" % guid)
    return guid

def createRacktivity(name, rackguid, login='root', password='rooter', ipaddress=None, port=6543, meteringdevicetype='racktivity'):
    masterguid = create(name, 'M1', rackguid, login=login, password=password, ipaddress=ipaddress, port=port, meteringdevicetype=meteringdevicetype)
    powermoduleguid = create("%s-power" % name, 'P1', rackguid, parentmeteringdeviceguid=masterguid, poweroutputsnumber=8,meteringdevicetype=meteringdevicetype)
    return masterguid, powermoduleguid

def delete(guid):
    cloudapi = p.api.action.racktivity
    cloudapi.meteringdevice.delete(guid)
    try:
        devices = cloudapi.meteringdevice.getObject(guid)
        raise RuntimeError("Meteringdevice '%s' didn't delete probably" % guid)
    except Fault:
        pass #success
        
