TAB_GENERAL_TITLE = 'General'

TAB_GENERAL_NAME = 'Name: '
TAB_GENERAL_PERMISSIONS = 'Permissions: '

TAB_GENERAL_NAME_HELPTEXT = 'Please provide the group\'s Name'
TAB_GENERAL_PERMISSIONS_HELPTEXT = 'Please provide the group\'s Permissions'

MSGBOX_CREATE_CONFIRMATION = "Update this group?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "group update"

MSGBOX_GROUP_CREATE_FAILED = "Failed to update this group! Please contact your system administrator!"
MSGBOX_GROUP_CREATE_FAILED_TITLE = "group update failed"


def callCloudAPI(api, **args):
    result = api.action.crm.group.update( **args)['result']    
    return result


def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)
    groupguid = params['groupguid']
    try:
        group = p.api.action.crm.group.getObject(groupguid, executionparams={'description': 'Retrieving group information'})
    except:
        q.logger.log('Error while Retrieving group %s information'% groupguid)

    fieldValue = group.name
    tab_general.addText(name ='name' 
                                      , text = TAB_GENERAL_NAME
                                      , helpText = TAB_GENERAL_NAME_HELPTEXT
                                      , value = fieldValue
                                      , optional = True
                                      
                                      )
    fieldValue = group.permissions
    tab_general.addText(name ='permissions' 
                                      , text = TAB_GENERAL_PERMISSIONS
                                      , helpText = TAB_GENERAL_PERMISSIONS_HELPTEXT
                                      , value = fieldValue
                                      , optional = True
                                      
                                      )
    
    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']
    cloudAPIArgs=dict()
    cloudAPIArgs['groupguid'] = groupguid
    
    cloudAPIArgs['name'] = str(tab_general.elements['name'].value)
    cloudAPIArgs['permissions'] = str(tab_general.elements['permissions'].value)
    result = callCloudAPI(p.api, **cloudAPIArgs)
    params['result'] = result

def match(q, i, p, params, tags):
	return True
