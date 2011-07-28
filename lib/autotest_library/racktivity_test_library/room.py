from pylabs import i,q,p

def create(name, datacenterguid, floorguid, tags = None):
    cloudapi = p.api.action.racktivity
    guid = cloudapi.room.create(name, datacenterguid=datacenterguid, floorguid=floorguid, tags = tags)['result']['roomguid']
    room = cloudapi.room.getObject(guid)
    if room.name != name:
        raise RuntimeError("Room wasn't created probably '%s'" % guid)
    return guid

def delete(guid):
    cloudapi = p.api.action.racktivity
    cloudapi.room.delete(guid)
    rooms = cloudapi.room.list(roomguid=guid)['result']['roominfo']
    if rooms:
        raise RuntimeError("Room '%s' didn't delete probably" % guid)
