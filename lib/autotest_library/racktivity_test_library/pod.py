from pylabs import i,q,p

def create(roomguid, name="test_pod1", description="pod 1 description"):
    ca = p.api.action.racktivity
    guid = ca.pod.create(name=name, description=description, roomguid=roomguid)['result']['podguid']
    pod = ca.pod.getObject(guid)
    if pod.name != name:
        raise Exception('pod %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = p.api.action.racktivity
    ca.pod.delete(guid)
    #Is it really gone?
    res = ca.pod.list(guid)['result']['podinfo']
    if len(res) > 0:
        raise Exception("Pod with guid %s still exists"%guid)
