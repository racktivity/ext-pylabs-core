from pylabs import q,i,p

def isAuthorized(login, drpobj, method):
    #get the user groups
    userguid = p.api.action.racktivity.clouduser.find(login = login)["result"]["guidlist"]
    if not userguid:
        raise ValueError("User with login %s was not found in clouduser list"%login)
    userguid = userguid[0]
    groups = p.api.action.racktivity.clouduser.listGroups(userguid)["result"]["groupinfo"][0]["groups"]
    #get the object's acl and do the validation
    if "cloudusergroupactions" in dir(drpobj):
        for group in groups:
            groupguid =  group["cloudusergroupguid"]
            if groupguid + "_" + method in drpobj.cloudusergroupactions:
                return True
        return False
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
