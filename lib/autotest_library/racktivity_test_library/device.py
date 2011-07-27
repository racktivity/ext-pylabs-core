from pylabs import i,q,p

def create(name, rackguid, devicetype='COMPUTER'):
    cloudapi = i.config.cloudApiConnection.find('main')
    guid = cloudapi.device.create(name, devicetype=devicetype, rackguid=rackguid)['result']['deviceguid']
    device = cloudapi.device.getObject(guid)
    if device.name != name:
        raise RuntimeError("Device wasn't created properly '%s'" % guid)
    return guid

def delete(guid):
    cloudapi = i.config.cloudApiConnection.find('main')
    cloudapi.device.delete(guid)
    devices = cloudapi.device.list(deviceguid=guid)['result']['deviceinfo']
    if devices:
        raise RuntimeError("Device '%s' didn't delete properly" % guid)