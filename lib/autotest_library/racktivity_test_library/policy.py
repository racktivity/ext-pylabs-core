from pylabs import i,q

def create(name = "TestPolicy"):
    ca = i.config.cloudApiConnection.find("main")
    guid = policy1Guid = ca.policy.create(name, "racktivity", "backup", None, 10)['result']['policyguid']
    policy = ca.policy.getObject(guid)
    if policy.name != name:
        raise Exception('policy %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = i.config.cloudApiConnection.find("main")
    ca.policy.delete(guid)
