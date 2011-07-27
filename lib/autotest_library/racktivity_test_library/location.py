from pylabs import i,q

def create(name="test_location1", description="Location 1 description", tags = None):
    ca = i.config.cloudApiConnection.find("main")
    guid = ca.location.create(name, description, tags = tags)['result']['locationguid']
    loc = ca.location.getObject(guid)
    if loc.name != name:
        raise Exception('location %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = i.config.cloudApiConnection.find("main")
    loc = ca.location.getObject(guid)
    ca.location.delete(guid)
    #Is it really gone?
    res = ca.location.list(guid)['result']['locationinfo']
    if len(res) > 0:
        raise Exception("Location with guid %s still exists"%guid)