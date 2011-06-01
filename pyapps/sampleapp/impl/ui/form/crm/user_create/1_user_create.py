TAB_GENERAL_TITLE = 'General'

TAB_GENERAL_PASSWORD = 'Password: '
TAB_GENERAL_NAME = 'Name: '
TAB_GENERAL_GROUPS = 'Groups: '

TAB_GENERAL_PASSWORD_HELPTEXT = 'Please provide the user\'s Password'
TAB_GENERAL_NAME_HELPTEXT = 'Please provide the user\'s Name'
TAB_GENERAL_GROUPS_HELPTEXT = 'Please provide the user\'s Groups'

MSGBOX_CREATE_CONFIRMATION = "Create this new User?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "user creation"

MSGBOX_USER_CREATE_FAILED = "Failed to create this new user! Please contact your system administrator!"
MSGBOX_USER_CREATE_FAILED_TITLE = "user creation failed"


def callCloudAPI(api, ** args):
   
    result = api.action.crm.user.create(** args)['result']    
    return result


def main(q, i, p, params, tags):
    
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)
    
    
    
    tab_general.addText(name ='password' 
                                      , text = TAB_GENERAL_PASSWORD
                                      , helpText = TAB_GENERAL_PASSWORD_HELPTEXT
                                      , optional = True
                                      
                                      )
    
    tab_general.addText(name ='name' 
                                      , text = TAB_GENERAL_NAME
                                      , helpText = TAB_GENERAL_NAME_HELPTEXT
                                      , optional = True
                                      
                                      )
    
    tab_general.addText(name ='groups' 
                                      , text = TAB_GENERAL_GROUPS
                                      , helpText = TAB_GENERAL_GROUPS_HELPTEXT
                                      , optional = True
                                      
                                      )

    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']
    cloudAPIArgs=dict()
    cloudAPIArgs['password'] = str(tab_general.elements['password'].value) 
    cloudAPIArgs['name'] = str(tab_general.elements['name'].value) 
    cloudAPIArgs['groups'] = str(tab_general.elements['groups'].value) 
        
    result = callCloudAPI(p.api, **cloudAPIArgs)
    params['result'] = result
