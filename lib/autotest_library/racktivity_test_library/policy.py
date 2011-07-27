from pylabs import i,q,p

def create(name = "TestPolicy"):
    ca = p.api.action.racktivity
    guid = policy1Guid = ca.policy.create(name, "racktivity", "backup", None, 10)['result']['policyguid']
    policy = ca.policy.getObject(guid)
    if policy.name != name:
        raise Exception('policy %s was not created properly'%guid)
    return guid

def delete(guid):
    ca = p.api.action.racktivity
    ca.policy.delete(guid)
