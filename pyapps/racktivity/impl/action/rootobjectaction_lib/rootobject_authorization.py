from pylabs import q,i

def isAuthorized(login, drpobj, method):
    #get the user groups
    userguid = q.actions.rootobject.clouduser.find(login = login)["result"]["guidlist"]
    if not userguid:
        raise ValueError("User with login %s was not found in clouduser list"%login)
    userguid = userguid[0]
    groups = q.actions.rootobject.clouduser.listGroups(userguid)["result"]["groupinfo"][0]["groups"]
    #get the object's acl and do the validation
    if "acl" in dir(drpobj) and drpobj.acl.cloudusergroupactions:
        acl = drpobj.acl
        for group in groups:
            groupguid =  group["cloudusergroupguid"]
            if groupguid + "_" + method in acl.cloudusergroupactions:
                return True
        return False
    #if no acl attribute or acl is None, return True
    return True

def getAuthorizedGuids(login, guidlist, drpclass, method):
    """
    Takes list of guids, return guids that is accessible by this user
    """
    result = list()
    for guid in guidlist:
        drpobj = drpclass.get(guid)
        if isAuthorized(login, drpobj, method):
            result.append(guid)
    return result
