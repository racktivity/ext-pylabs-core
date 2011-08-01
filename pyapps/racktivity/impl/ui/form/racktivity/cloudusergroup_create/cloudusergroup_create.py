__tags__ = 'wizard','cloudusergroup_create'
__author__ = 'racktivity'


CUG_ADDG_TITLE = "Create Cloud User Group"
CUG_NAME = "Cloud User Group name"
CUG_NAME_HELP = "Enter a name for the cloud user group that you want to create"
CUG_DESCRIPTION = "Cloud User Group description"
CUG_DESCRIPTION_HELP = "Enter a description text for the cloud user group that you want to create"
ERROR_CUG_NAME = "Invalid cloud user group name"
ERROR_CUG_DESC = "Invalid cloud user group description text"
  

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

    cloudapi = i.config.cloudApiConnection.find('main')
    
    currentlogin = params['extra']['login']
    if not inGroup(cloudapi, currentlogin, "administrators"):
        q.gui.dialog.showMessageBox("You don't have permissin to do this action",
                                    "Permission Denied", msgboxIcon="Error")
        return
    
    form = q.gui.form.createForm()

    tabMain = form.addTab('tabMain',CUG_ADDG_TITLE)
    tabMain.addText('racktivity_cloudusergroup_name', 
                CUG_NAME,
                helpText=CUG_NAME_HELP,
                optional=False)
    
    tabMain.addMultiline('racktivity_cloudusergroup_desc', 
                CUG_DESCRIPTION,
                helpText=CUG_DESCRIPTION_HELP)

    form.loadForm(q.gui.dialog.askForm(form))
    tab = form.tabs['tabMain']
    name = tab.elements['racktivity_cloudusergroup_name'].value
    desc = tab.elements['racktivity_cloudusergroup_desc'].value
    apicallresult = cloudapi.cloudusergroup.create(name = name, description = desc)
    
    q.gui.dialog.showMessageBox("Cloud user group '%s' is being created" % name, "Create Cloud user group")

def main(q, i, p, params, tags):
    return True
