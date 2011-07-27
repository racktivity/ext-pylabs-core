from pylabs import i,q,p

def create(name, roomguid, racktype='OPEN', tags = None):
    cloudapi = i.config.cloudApiConnection.find('main')
    guid = cloudapi.rack.create(name, racktype=racktype, roomguid=roomguid, tags = tags)['result']['rackguid']
    rack = cloudapi.rack.getObject(guid)
    if rack.name != name:
        raise RuntimeError("Rack wasn't created probably '%s'" % guid)
    return guid

def delete(guid):
    cloudapi = i.config.cloudApiConnection.find('main')
    cloudapi.rack.delete(guid)
    racks = cloudapi.rack.list(rackguid=guid)['result']['rackinfo']
    if racks:
        raise RuntimeError("Rack '%s' didn't delete probably" % guid)