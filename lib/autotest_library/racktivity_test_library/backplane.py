from pylabs import i,q,p

def create(name = "test_backplane1", backplanetype = 'INFINIBAND', description='test_backplane1_description'):
    ca = p.api.action.racktivity
    guid = ca.backplane.create(name, backplanetype, description)['result']['backplaneguid']
    backplane = ca.backplane.getObject(guid)
    if backplane.name != name:
        raise Exception('backplane %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = p.api.action.racktivity
    #Delete the backplane first
    ca.backplane.delete(guid)
    #Is it really gone?
    res = ca.backplane.list(guid)['result']['backplaneinfo']
    if len(res) > 0:
        raise Exception("Backplane with guid %s still exists"%guid)
