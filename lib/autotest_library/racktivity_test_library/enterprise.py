from pylabs import i,q

def create(name="Enterprise1", description="enterprise 1 description", tags=None):
    ca = i.config.cloudApiConnection.find("main")
   
    guid = ca.enterprise.create(name=name, description=description, tags=tags)['result']['enterpriseguid']
    enterprise = ca.enterprise.getObject(guid)
    if enterprise.name != name:
        raise Exception('enterprise %s was not created properly'%guid)
    return guid

def delete(guid):
    """
    @param guid:    enterprise guid
    """
    ca = i.config.cloudApiConnection.find("main")
    #Delete the enterprise
    ca.enterprise.delete(guid)
    #Is it really gone?
    res = ca.enterprise.list(guid)['result']['enterpriseinfo']
    if len(res) > 0:
        raise Exception("Enterprise with guid %s still exists"%guid)
