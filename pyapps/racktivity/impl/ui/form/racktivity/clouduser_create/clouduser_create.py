__author__ = 'racktivity'
__tags__ = 'wizard', 'clouduser_create'

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
    
    form = q.gui.form.createForm()
    generaltab = form.addTab('generaltab', 'General')
    generaltab.addText('login', 'Login:', message='Please specify user login', optional=False, validator="^[a-zA-Z0-9]{1,16}$")
    generaltab.addPassword('password', 'Password: ', message='Please specify user password', optional=False)
    generaltab.addPassword('password_validation', 'Confirm Password: ', message='Please re-enter your password', optional=False)
    generaltab.addText('email', 'Email Address: ', message='Please enter user email address', \
                       validator="^\w+(\.\w+)*@\w+(\.\w+)+$", helpText='e.g. john.smith@example.com')
    generaltab.addText('firstname', 'First Name: ', message='Please enter user first name',
                       helpText='Please provide user first name, allowed characters are A to Z and 0 to 9')
    generaltab.addText('lastname', 'Last Name: ', message='Please enter user last name',
                       helpText='Please provide user last name, allowed characters are A to Z and 0 to 9')
    generaltab.addMultiline('description', 'Description: ', message='Please enter the user description')
    generaltab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    generaltab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')
    
    cloudusergroups = cloudapi.cloudusergroup.list()['result']['cloudusergroupinfo']
    cloudusergroupDict = dict([(ug['guid'], ug['name']) for ug in cloudusergroups])
    generaltab.addChoiceMultiple('usergroup', 'User Group: ', cloudusergroupDict, selectedValue='', optional=True)

    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        tab = form.tabs['generaltab']
        login = tab.elements['login'].value
        tags = tab.elements['tags'].value
        if cloudapi.clouduser.find(login=login)['result']['guidlist']:
            tab.elements['login'].message = 'A user with the same login already exists'
            tab.elements['login'].status = 'error'
        elif tab.elements['password'].value != tab.elements['password_validation'].value:
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

    clouduser = cloudapi.clouduser.create(login=tab.elements['login'].value,
                              password=tab.elements['password'].value,
                              email=tab.elements['email'].value,
                              firstname=tab.elements['firstname'].value,
                              lastname=tab.elements['lastname'].value,
                              description=tab.elements['description'].value,
                              tags=tagstring)
    clouduserguid = clouduser['result']['clouduserguid']

    confluenceuser = q.config.getConfig('confluence')['main']['login']
    confluencepassword = q.config.getConfig('confluence')['main']['password']
    q.clients.confluence.connect('http://localhost:8080/confluence', confluenceuser, confluencepassword)
    newuser = tab.elements['login'].value
    password = tab.elements['password'].value
    try:
        q.clients.confluence.addUser(newuser, newuser, password)
        q.clients.confluence.addUserToGroup(newuser, 'confluence-administrators')
    finally:
        q.clients.confluence.logout()
    
    #Add clouduser to the chosen cloudusergroups
    
    for group in tab.elements['usergroup'].value:
        cloudapi.cloudusergroup.addUser(group, clouduserguid)
        
    q.gui.dialog.showMessageBox('Cloud user "%s" is being created' % tab.elements['login'].value, "Create Cloud user")

def main(q, i, p, params, tags):
    return True
