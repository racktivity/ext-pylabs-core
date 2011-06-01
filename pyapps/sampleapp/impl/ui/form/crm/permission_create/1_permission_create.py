TAB_GENERAL_TITLE = 'General'

TAB_GENERAL_NAME = 'Name: '
TAB_GENERAL_URI = 'Uri: '

TAB_GENERAL_NAME_HELPTEXT = 'Please provide the permission\'s Name'
TAB_GENERAL_URI_HELPTEXT = 'Please provide the permission\'s Uri'

MSGBOX_CREATE_CONFIRMATION = "Create this new Permission?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "permission creation"

MSGBOX_PERMISSION_CREATE_FAILED = "Failed to create this new permission! Please contact your system administrator!"
MSGBOX_PERMISSION_CREATE_FAILED_TITLE = "permission creation failed"


def callCloudAPI(api, ** args):
   
    result = api.action.crm.permission.create(** args)['result']    
    return result


def main(q, i, p, params, tags):
    
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)
    
    
    
    tab_general.addText(name ='name' 
                                      , text = TAB_GENERAL_NAME
                                      , helpText = TAB_GENERAL_NAME_HELPTEXT
                                      , optional = True
                                      
                                      )
    
    tab_general.addText(name ='uri' 
                                      , text = TAB_GENERAL_URI
                                      , helpText = TAB_GENERAL_URI_HELPTEXT
                                      , optional = True
                                      
                                      )

    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']
    cloudAPIArgs=dict()
    cloudAPIArgs['name'] = str(tab_general.elements['name'].value) 
    cloudAPIArgs['uri'] = str(tab_general.elements['uri'].value) 
        
    result = callCloudAPI(p.api, **cloudAPIArgs)
    params['result'] = result
