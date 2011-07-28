from pylabs import i,q,p

def create(name, roomguid=None, racktype='OPEN', podguid=None, rowguid=None, tags = None):
    cloudapi = p.api.action.racktivity
    guid = cloudapi.rack.create(name, racktype=racktype, roomguid=roomguid,podguid=podguid,rowguid=rowguid, tags = tags)['result']['rackguid']
    rack = cloudapi.rack.getObject(guid)
    if rack.name != name:
        raise RuntimeError("Rack wasn't created probably '%s'" % guid)
    return guid

def delete(guid):
    cloudapi = p.api.action.racktivity
    cloudapi.rack.delete(guid)
    racks = cloudapi.rack.list(rackguid=guid)['result']['rackinfo']
    if racks:
        raise RuntimeError("Rack '%s' didn't delete probably" % guid)
