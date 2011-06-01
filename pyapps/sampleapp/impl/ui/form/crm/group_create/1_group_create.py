TAB_GENERAL_TITLE = 'General'

TAB_GENERAL_NAME = 'Name: '
TAB_GENERAL_PERMISSIONS = 'Permissions: '

TAB_GENERAL_NAME_HELPTEXT = 'Please provide the group\'s Name'
TAB_GENERAL_PERMISSIONS_HELPTEXT = 'Please provide the group\'s Permissions'

MSGBOX_CREATE_CONFIRMATION = "Create this new Group?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "group creation"

MSGBOX_GROUP_CREATE_FAILED = "Failed to create this new group! Please contact your system administrator!"
MSGBOX_GROUP_CREATE_FAILED_TITLE = "group creation failed"


def callCloudAPI(api, ** args):
   
    result = api.action.crm.group.create(** args)['result']    
    return result


def main(q, i, p, params, tags):
    
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)
    
    
    
    tab_general.addText(name ='name' 
                                      , text = TAB_GENERAL_NAME
                                      , helpText = TAB_GENERAL_NAME_HELPTEXT
                                      , optional = True
                                      
                                      )
    
    tab_general.addText(name ='permissions' 
                                      , text = TAB_GENERAL_PERMISSIONS
                                      , helpText = TAB_GENERAL_PERMISSIONS_HELPTEXT
                                      , optional = True
                                      
                                      )

    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']
    cloudAPIArgs=dict()
    cloudAPIArgs['name'] = str(tab_general.elements['name'].value) 
    cloudAPIArgs['permissions'] = str(tab_general.elements['permissions'].value) 
        
    result = callCloudAPI(p.api, **cloudAPIArgs)
    params['result'] = result
