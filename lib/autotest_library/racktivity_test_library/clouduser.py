from pylabs import i,q

def create(login="test_clouduser1",password="123", description="clouduser 1 description", groupguid = None):
    ca = i.config.cloudApiConnection.find("main")
    guid = ca.clouduser.create(login, password, description=description)['result']['clouduserguid']
    if groupguid:
        ca.cloudusergroup.addUser(guid, groupguid)
    usr = ca.clouduser.getObject(guid)
    if usr.login != login:
        raise Exception('User %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = i.config.cloudApiConnection.find("main")
    usr = ca.clouduser.getObject(guid)
    ca.clouduser.delete(guid)
    #Is it really gone?
    res = ca.clouduser.list(guid)['result']['clouduserinfo']
    if len(res) > 0:
        raise Exception("Clouduser with guid %s still exists"%guid)
