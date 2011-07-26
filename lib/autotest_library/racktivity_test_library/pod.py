from pylabs import i,q

def create(roomguid, name="test_pod1", description="pod 1 description", racks = []):
    ca = i.config.cloudApiConnection.find("main")
    guid = ca.pod.create(name=name, description=description, room=roomguid, racks = racks)['result']['podguid']
    pod = ca.pod.getObject(guid)
    if pod.name != name:
        raise Exception('pod %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = i.config.cloudApiConnection.find("main")
    ca.pod.delete(guid)
    #Is it really gone?
    res = ca.pod.list(guid)['result']['podinfo']
    if len(res) > 0:
        raise Exception("Pod with guid %s still exists"%guid)
