from pylabs import i,q

def create(name, datacengerguid, floor=0):
    ca = i.config.cloudApiConnection.find("main")
    floorguid = ca.floor.create(name, floor, datacengerguid)['result']['floorguid']
    floorobj = ca.floor.getObject(floorguid)
    if floorobj.name != name:
        raise Exception('floor %s was not created properly'%floorguid)
    
    return floorguid

def delete(guid):
    """
    @param guid:    datacenter guid
    @param delLocation:    set to True to delete the location attached to this data center
    @param delCloudUser:    set to True to delete the clouduser attached to this data center (has no effect if no user attached)
    """
    ca = i.config.cloudApiConnection.find("main")
    ca.floor.delete(guid)
    #Is it really gone?
    res = ca.floor.list(guid)['result']['floorinfo']
    if len(res) > 0:
        raise Exception("Floor with guid %s still exists"%guid)
