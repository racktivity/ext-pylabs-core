__author__ = 'racktivity'
__tags__ = 'wizard', 'clouduser_delete'

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
    
    clouduserguid = params['extra']['rootobjectguid']
    clouduser = cloudapi.clouduser.getObject(clouduserguid)
    
    msg = "Are you sure you want to delete user '%s'?" % clouduser.name
    answer = q.gui.dialog.showMessageBox(msg, "Delete cloud user", msgboxButtons="YesNo",
                                             msgboxIcon="Question", defaultButton="No")
    if answer == "NO":
        return
    
    
    cloudapi.clouduser.delete(clouduserguid)
    confluenceuser = q.config.getConfig('confluence')['main']['login']
    confluencepassword = q.config.getConfig('confluence')['main']['password']
    q.clients.confluence.connect('http://localhost:8080/confluence', confluenceuser, confluencepassword)
    try:
        q.clients.confluence.removeUser(clouduser.login)
    except:
        pass
    finally:
        q.clients.confluence.logout()
    
    q.gui.dialog.showMessageBox("cloud user '%s' has been deleted" % clouduser.login, "Delete cloud user")
    
def match(q, i, p, params, tags):
    return True
