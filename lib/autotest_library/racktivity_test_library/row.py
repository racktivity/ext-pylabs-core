from pylabs import i,q

def create(podguid, name="test_row1", description="row 1 description", racks = []):
    ca = i.config.cloudApiConnection.find("main")
    pod = ca.pod.getObject(podguid)
    guid = ca.row.create(name, description = description, pod = pod.guid, room = pod.room, racks = racks)['result']['rowguid']
    row = ca.row.getObject(guid)
    if row.name != name:
        raise Exception('row %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = i.config.cloudApiConnection.find("main")
    ca.row.delete(guid)
    #Is it really gone?
    res = ca.row.list(guid)['result']['rowinfo']
    if len(res) > 0:
        raise Exception("row with guid %s still exists"%guid)
