TAB_GENERAL_TITLE = 'General'

TAB_GENERAL_PASSWORD = 'Password: '
TAB_GENERAL_NAME = 'Name: '
TAB_GENERAL_GROUPS = 'Groups: '

TAB_GENERAL_PASSWORD_HELPTEXT = 'Please provide the user\'s Password'
TAB_GENERAL_NAME_HELPTEXT = 'Please provide the user\'s Name'
TAB_GENERAL_GROUPS_HELPTEXT = 'Please provide the user\'s Groups'

MSGBOX_CREATE_CONFIRMATION = "Update this user?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "user update"

MSGBOX_USER_CREATE_FAILED = "Failed to update this user! Please contact your system administrator!"
MSGBOX_USER_CREATE_FAILED_TITLE = "user update failed"


def callCloudAPI(api, **args):
    result = api.action.crm.user.update( **args)['result']    
    return result


def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)
    userguid = params['userguid']
    try:
        user = p.api.action.crm.user.getObject(userguid, executionparams={'description': 'Retrieving user information'})
    except:
        q.logger.log('Error while Retrieving user %s information'% userguid)

    fieldValue = user.password
    tab_general.addText(name ='password' 
                                      , text = TAB_GENERAL_PASSWORD
                                      , helpText = TAB_GENERAL_PASSWORD_HELPTEXT
                                      , value = fieldValue
                                      , optional = True
                                      
                                      )
    fieldValue = user.name
    tab_general.addText(name ='name' 
                                      , text = TAB_GENERAL_NAME
                                      , helpText = TAB_GENERAL_NAME_HELPTEXT
                                      , value = fieldValue
                                      , optional = True
                                      
                                      )
    fieldValue = user.groups
    tab_general.addText(name ='groups' 
                                      , text = TAB_GENERAL_GROUPS
                                      , helpText = TAB_GENERAL_GROUPS_HELPTEXT
                                      , value = fieldValue
                                      , optional = True
                                      
                                      )
    
    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']
    cloudAPIArgs=dict()
    cloudAPIArgs['userguid'] = userguid
    
    cloudAPIArgs['password'] = str(tab_general.elements['password'].value)
    cloudAPIArgs['name'] = str(tab_general.elements['name'].value)
    cloudAPIArgs['groups'] = str(tab_general.elements['groups'].value)
    result = callCloudAPI(p.api, **cloudAPIArgs)
    params['result'] = result

def match(q, i, p, params, tags):
	return True
