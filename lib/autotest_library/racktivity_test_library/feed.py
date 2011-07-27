from pylabs import i,q,p

def create(name, datacenterguid):
    cloudapi = i.config.cloudApiConnection.find('main')
    guid = cloudapi.feed.create(name, "COAL", datacenterguid)['result']['feedguid']
    feed = cloudapi.feed.getObject(guid)
    if feed.name != name:
        raise RuntimeError("Feed wasn't created probably '%s'" % guid)
    return guid

def delete(guid):
    cloudapi = i.config.cloudApiConnection.find('main')
    cloudapi.feed.delete(guid)
    feeds = cloudapi.feed.list(feedguid=guid)['result']['feedinfo']
    if feeds:
        raise RuntimeError("Feed '%s' didn't delete probably" % guid)