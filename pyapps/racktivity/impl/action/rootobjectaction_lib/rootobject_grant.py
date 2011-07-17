from pymonkey import q
from rootobjectaction_lib import rootobjectaction_find, rootobjectaction_list
 
def grantUser(rootobjectguid, rootobjecttype, cloudusername):
    """

    grants access to all actions of the given rootobject instance to the cloudusergroup of the cloudusername

    """
    drpobject = getattr(q.drp, rootobjecttype)
    rootobjectinstance = drpobject.get(rootobjectguid)
    acl = rootobjectinstance.acl
    if not acl:
        acl = rootobjectinstance.acl.new()
        rootobjectinstance.acl = acl
        drpobject.save(rootobjectinstance)

    clouduserguids = rootobjectaction_find.clouduser_find(login=cloudusername)
    if not clouduserguids:
        q.logger.log("Invalid cloud user name passed to grantUser function")
        return
    clouduserguid = clouduserguids[0]
    cloudusergroups = rootobjectaction_list.clouduser_list(clouduserguid)
    if not cloudusergroups:
        q.logger.log("Could not get the cloudusergroup for the cloud user %s" % clouduserguid)
        return
    groups = cloudusergroups[0]['groups']
    if not groups:
        q.logger.log("The group list for the cloud user %s is empty" % clouduserguid)
        return
    actions = dir(getattr(q.actions.rootobject, rootobjecttype))
    for group in groups:
        for action in actions:
            if action.startswith("_"):
                continue
            acl.cloudusergroupactions[group['guid']+"_"+action] = ""
    drpobject.save(rootobjectinstance)