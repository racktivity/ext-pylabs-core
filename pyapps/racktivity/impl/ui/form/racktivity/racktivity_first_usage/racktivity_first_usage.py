__tags__ = "wizard", "racktivity_first_usage"
__author__ = "racktivity"

BACKUP_POLICY = 'racktivity_backup'

def getTagString(q, tab):
    labels = None
    labelsvalue = tab.elements['labels'].value
    trim = lambda s: s.strip()
    if labelsvalue:
        labels = set(map(trim, labelsvalue.split(',')))

    tags = dict()
    tagsvalue = tab.elements['tags'].value
    if tagsvalue:
        for tag in map(trim, tagsvalue.split(',')):
            tagslist = tag.split(':')
            tags[tagslist[0].strip()] = tagslist[1].strip()
    return q.base.tags.getTagString(labels, tags)

def main(q, i, p, params, tags):
    import json
    cloudapi = p.api.action.racktivity
    form = q.gui.form.createForm()
    
    tab = form.addTab("main", "First Usage")
    tab.message("m1", "Mail information", bold=True)
    tab.addText("smtp_server", "SMTP Server", optional=False)
    tab.addText("smtp_login", "SMTP Login", optional=False)
    tab.addPassword("smtp_password", "SMTP Password", optional=False)
    
    tab.message("m2", "UI information", bold=True)
    tab.addText("ui_login", "UI Login", optional=False)
    tab.addPassword("ui_password", "UI Password", optional=False)
    
    enterprisetab = form.addTab('enterprise', 'Enterprise')
    enterprisetab.addText('name', 'Name', message='Please enter the enterprise name', optional=False)
    enterprisetab.addMultiline('description', 'Description', message='Please enter the enterprise description')
    enterprisetab.addText('tags', 'Tags', helpText='Enter tags in the form of tag1:value1,tag2:value2')
    enterprisetab.addText('labels', 'Labels', helpText='Enter labels as comma separated values e.g. label1,label2')
    
    backuptab = form.addTab('backup', 'Backup Configuration')
    backuptab.addText('location', 'Backup location', value='/opt/racktivity_backups', message='Please enter the backup location')
    backuptab.addInteger('interval', 'Time between backups in hours', value=24, helpText='Enter the time in hours between backups', minValue=1)
    
    valid = False
    while not valid:
        form.loadForm(q.gui.dialog.askForm(form))
        #validate data
        tab = form.tabs['main']
        valid = True
    tab = form.tabs['main']
    swversion = q.config.getConfig('swversion')['main']['swversion']
    cloudapi.racktivity.create(sw_version=swversion, smtp=tab.elements['smtp_server'].value, smtplogin=tab.elements['smtp_login'].value, smtppassword=tab.elements['smtp_password'].value, configured=True)
    
    
    confluenceuser = q.config.getConfig('confluence')['main']['login']
    confluencepassword = q.config.getConfig('confluence')['main']['password']
    q.clients.confluence.connect('http://localhost:8080/confluence', confluenceuser, confluencepassword)
    q.clients.confluence.removeUser('first_login')
    newuser = tab.elements['ui_login'].value
    password = tab.elements['ui_password'].value
    try:
        q.clients.confluence.removeUser(newuser)
    except:
        pass
    try:
        q.clients.confluence.addUser(newuser, newuser, password)
        q.clients.confluence.addUserToGroup(newuser, 'confluence-administrators')
    finally:
        q.clients.confluence.logout()
     
    #create the user and add it to the admin groups
    admingroupguid = cloudapi.cloudusergroup.find(name="administrators")['result']['guidlist'][0]
    userguid = cloudapi.clouduser.create(newuser, password)['result']['clouduserguid']
    cloudapi.cloudusergroup.addUser(admingroupguid, userguid)
    
    enterprisetab = form.tabs['enterprise']
    tagstring = getTagString(q, enterprisetab)
    result = cloudapi.enterprise.create(name=enterprisetab.elements['name'].value,
                                             description=enterprisetab.elements['description'].value,
                                             tags=tagstring)

    backuppolicyguids = cloudapi.policy.find(BACKUP_POLICY)['result']['guidlist']
    tab = form.tabs['backup'] 
    if backuppolicyguids:
        #The backup policy already exists
        backuppolicyguid = backuppolicyguids[0]
        cloudapi.policy.updateModelProperties(backuppolicyguid, name = BACKUP_POLICY, \
                             policyparams=json.dumps({'path':tab.elements['location'].value }), interval=float(tab.elements['interval'].value)*60)
    else:
        #Create the backup policy
        cloudapi.policy.create(name = BACKUP_POLICY, description = 'Racktivity Backup policy', \
                                                                 interval = float(tab.elements['interval'].value)*60, \
                                                                 rootobjecttype = 'racktivity', rootobjectaction = 'backup', \
                                                                 runbetween = '[("00:00", "24:00")]', runnotbetween = '[]', \
								 rootobjectguid = None, \
                                                                 policyparams = json.dumps({'path':tab.elements['location'].value }))

    q.gui.dialog.showMessageBox("New user has been created successfull please relogin using this user", "Information")

def main(q, i, p, params, tags):
    return True
