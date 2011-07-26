from pylabs import i,q
import uuid

def create(name="Datacenter1", locationguid=None, description="Datacenter 1 description", clouduserguid=None, tags=None):
    ca = i.config.cloudApiConnection.find("main")
    if locationguid is None:
        locationguid = ca.location.create(str(uuid.uuid4()))['result']['locationguid']
    guid = ca.datacenter.create(name, locationguid, description, clouduserguid, tags = tags)['result']['datacenterguid']
    dc = ca.datacenter.getObject(guid)
    if dc.name != name:
        raise Exception('datacenter %s was not created properly'%guid)
    return guid

def delete(guid, delLocation = False, delCloudUser = False):
    """
    
    @param guid:    datacenter guid
    @param delLocation:    set to True to delete the location attached to this data center
    @param delCloudUser:    set to True to delete the clouduser attached to this data center (has no effect if no user attached)
    """
    ca = i.config.cloudApiConnection.find("main")
    dc = ca.datacenter.getObject(guid)
    locGuid = dc.locationguid
    usrGuid = dc.clouduserguid
    #Delete the datacenter first
    ca.datacenter.delete(guid)
    #Is it really gone?
    res = ca.datacenter.list(guid)['result']['datacenterinfo']
    if len(res) > 0:
        raise Exception("Datacenter with guid %s still exists"%guid)
    
    if delLocation:
        ca.location.delete(locGuid)
    if delCloudUser and usrGuid:
        ca.clouduser.delete(usrGuid)
