__author__ = 'racktivity'
__tags__ = 'wizard','cloudusergroup_delete'


def inGroup(cloudapi, login, *groups):
    guids = cloudapi.clouduser.find(login=login)['result']['guidlist']
    
    if not guids or not groups:
        return False
    
    groupsinfo = cloudapi.clouduser.listGroups(guids[0])['result']['groupinfo']
    availablegroups = list()
    for groupinfo in groupsinfo:
        availablegroups += map(lambda g: g['name'], groupinfo['groups'])
    
    for group in groups:
        if group not in availablegroups:
            return False
    return True

def main(q, i, p, params, tags):
    cloudapi = p.api.action.racktivity
    
    currentlogin = params['extra']['login']
    if not inGroup(cloudapi, currentlogin, "administrators"):
        q.gui.dialog.showMessageBox("You don't have permissin to do this action",
                                    "Permission Denied", msgboxIcon="Error")
        return
    
    cloudusergroupguid = params['extra']['rootobjectguid']
    cloudusergroup = cloudapi.cloudusergroup.getObject(cloudusergroupguid)
    msg = "Are you sure you want to delete user group '%s'?" % cloudusergroup.name
    
    answer = q.gui.dialog.showMessageBox(msg, "Delete Cloud user group", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
    if answer == "NO":
        return
    
    
    
    cloudapi.cloudusergroup.delete(cloudusergroupguid)
    q.gui.dialog.showMessageBox("Cloud user group '%s' is being deleted" % cloudusergroup.name, "Delete Cloud user group")
    
def match(q, i, p, params, tags):
    return True
