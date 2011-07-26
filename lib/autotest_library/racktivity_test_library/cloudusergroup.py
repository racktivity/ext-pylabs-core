from pylabs import i,q

def create(name="test_clouduser1",password="123", description="clouduser 1 description"):
    ca = i.config.cloudApiConnection.find("main")
    guid = ca.cloudusergroup.create(name,description)['result']['cloudusergroupguid']
    grp = ca.cloudusergroup.getObject(guid)
    if grp.name != grp:
        raise Exception('Group %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = i.config.cloudApiConnection.find("main")
    grp = ca.cloudusergroup.getObject(guid)
    ca.cloudusergroup.delete(guid)
    #Is it really gone?
    res = ca.cloudusergroup.list(cloudusergroupguid = guid)['result']['cloudusergroupinfo']
    if len(res) > 0:
        raise Exception("Cloudusergroup with guid %s still exists"%guid)
