__author__ = 'racktivity'
__tags__ = 'wizard', 'clouduser_update'

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
    
    clouduserguid = params['extra']['rootobjectguid']
    clouduser = cloudapi.clouduser.getObject(clouduserguid) 
    
    currentlogin = params['extra']['login']
    isadmin = inGroup(cloudapi, currentlogin, "administrators")
    if not isadmin and clouduser.login != currentlogin:
        q.gui.dialog.showMessageBox("You don't have permissin to do this action",
                                    "Permission Denied", msgboxIcon="Error")
        return
    
    
    form = q.gui.form.createForm()
    
    
    
    generaltab = form.addTab('generaltab', 'General')
    generaltab.message('login', 'Login: %s' % clouduser.login, bold=True)
    generaltab.addPassword('password', 'Password: ', message='Please specify user password', 
                           value=clouduser.password, optional=False)
    generaltab.addPassword('password_validation', 'Confirm Password: ', message='Please re-enter your password',
                           value=clouduser.password, optional=False)
    generaltab.addText('email', 'Email Address: ', message='Please enter user email address', value=clouduser.email,
                       validator="^\w+(\.\w+)*@\w+(\.\w+)+$", helpText='e.g. john.smith@example.com')
    generaltab.addText('firstname', 'First Name: ', message='Please enter user first name', value=clouduser.firstname,
                       helpText='Please provide user first name, allowed characters are A to Z and 0 to 9')
    generaltab.addText('lastname', 'Last Name: ', message='Please enter user last name', value=clouduser.lastname,
                       helpText='Please provide user last name, allowed characters are A to Z and 0 to 9')
    
    generaltab.addMultiline('description', 'Description: ', message='Please enter the user description', value=clouduser.description)
    
    cloudusergroups = cloudapi.cloudusergroup.list()['result']['cloudusergroupinfo']
    cloudusergroupDict = dict([(ug['guid'], ug['name']) for ug in cloudusergroups])
    
    if isadmin:
        usergroups = cloudapi.clouduser.listGroups(clouduser.guid)['result']['groupinfo'][0]['groups']
        usergroupsguids = [ug['cloudusergroupguid'] for ug in usergroups]
        generaltab.addChoiceMultiple('usergroup', 'User Group: ', cloudusergroupDict, selectedValue='', optional=True)
        generaltab.elements['usergroup'].value = usergroupsguids

    generaltab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    generaltab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')
    
    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['generaltab']
        tags = tab.elements['tags'].value
        if tab.elements['password'].value != tab.elements['password_validation'].value:
            tab.elements['password'].message = tab.elements['password_validation'].message = 'passwords do not match'
            tab.elements['password'].status = tab.elements['password_validation'].status = 'error'
        elif tags and ':' not in tags:
            tab.elements['tags'].message = 'Tags have to be given in the form of tag1:value1,tag2:value2'
            tab.elements['tags'].status = 'error'
        else:
            valid = True

    tab = form.tabs['generaltab']

    labels = None
    labelsvalue = tab.elements['labels'].value
    if labelsvalue:
        labels = set(labelsvalue.split(','))

    tags = dict()
    tagsvalue = tab.elements['tags'].value
    if tagsvalue:
        for tag in tagsvalue.split(','):
            tagslist = tag.split(':')
            tags[tagslist[0]] = tagslist[1]
    tagstring = q.base.tags.getTagString(labels, tags)

    cloudapi.clouduser.updateModelProperties(clouduser.guid,
                              email=tab.elements['email'].value,
                              firstname=tab.elements['firstname'].value,
                              lastname=tab.elements['lastname'].value,
                              description=tab.elements['description'].value,
                              tags=tagstring)
    
    if clouduser.password != tab.elements['password'].value:
        cloudapi.clouduser.updatePassword(clouduser.guid, clouduser.password, tab.elements['password'].value)
    
    if isadmin:
        toadd = set(tab.elements['usergroup'].value).difference(usergroupsguids)
        toremove = set(usergroupsguids).difference(tab.elements['usergroup'].value)
        
        for group in toremove:
            #remove them
            cloudapi.cloudusergroup.removeUser(group, clouduser.guid)
        
        for group in toadd:
            #add them
            cloudapi.cloudusergroup.addUser(group, clouduser.guid)
    
    q.gui.dialog.showMessageBox('Cloud user "%s" has been updated' % clouduser.login, "Update Cloud user")

def match(q, i, p, params, tags):
    return True
