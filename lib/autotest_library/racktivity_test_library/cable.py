from pylabs import i,q

def create(name = "test_cable1", cabletype = 'POWERCABLE', description='test_cable1_description', label='cable1label'):
    ca = i.config.cloudApiConnection.find("main")
    guid = ca.cable.create(name, cabletype, description, label)['result']['cableguid']
    cable = ca.cable.getObject(guid)
    if cable.name != name:
        raise Exception('cable %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = i.config.cloudApiConnection.find("main")
    #Delete the cable first
    ca.cable.delete(guid)
    #Is it really gone?
    res = ca.cable.list(guid)['result']['cableinfo']
    if len(res) > 0:
        raise Exception("Cable with guid %s still exists"%guid)
