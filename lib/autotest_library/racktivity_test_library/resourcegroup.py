from pylabs import i,q

def create(name="test_resourcegroup1", description="Resourcegroup 1 description"):
    ca = i.config.cloudApiConnection.find("main")
    guid = ca.resourcegroup.create(name, description)['result']['resourcegroupguid']
    resg = ca.resourcegroup.getObject(guid)
    if resg.name != name:
        raise Exception('resourcegroup %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = i.config.cloudApiConnection.find("main")
    resg = ca.resourcegroup.getObject(guid)
    ca.resourcegroup.delete(guid)
    #Is it really gone?
    res = ca.resourcegroup.list(guid)['result']['resourcegroupinfo']
    if len(res) > 0:
        raise Exception("Resourcegroup with guid %s still exists"%guid)