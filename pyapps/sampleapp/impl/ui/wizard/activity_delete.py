__tags__ = 'wizard', 'activity', 'create'
__author__ = 'incubaid'

TAB_GENERAL_TITLE = 'Delete Activity'
TAB_GENERAL_ACTIVITY = 'Select Activity : '
TAB_CONFIRM_TITLE = 'Confirmation'
TAB_CONFIRM_TEXT = 'Are you sure you want to delete the activity? '
SELECT_ACTIVITIES  = 'Select the activities to be deleted '

NO_ACTIVITIES_TITLE = 'No Activities'
NO_ACTIVITIES_MESSAGE = 'No activities available in database'
NO_ACTIVITIES_SELECTED = 'No activities selected'

MSGBOX_CONFIRMATION = 'Delete activity?' 
MSGBOX_CONFIRMATION_TITLE = 'Delete activity?'


def callCloudAPI(api, activityguid):
    result = api.crm.activity.delete(activityguid)['result']
    return result

def getActivities(q, api):
    activities = dict()
    result = api.action.crm.activity.list()['result']
    
    map(lambda x: activities.__setitem__(x['guid'], x['name']), result)
    return activities

def main(q, i, p, params, tags):
    
    cloudAPI = i.config.cloudApiConnection.find('main')
    cloudAPI.setCredentials(params['login'],params['password'])
    
    activities = getActivities(q, cloudAPI)
    
    form = q.gui.form.createForm()
    tab_general = form.addTab('general', TAB_GENERAL_TITLE)
    if len(activities) > 0:
        tab_general.addChoiceMultiple('select', 
                                      SELECT_ACTIVITIES, 
                                      activities, 
                                      selectedValue = "",
                                      helpText = SELECT_ACTIVITIES)
    else:
        q.gui.dialog.showMessageBox(message = NO_ACTIVITIES_MESSAGE, 
                                    title = NO_ACTIVITIES_TITLE, 
                                    msgboxButtons = 'OK',
                                    defaultButton = 'OK',
                                    msgboxIcon = 'Error')
        return
    
    form.loadForm(q.gui.dialog.askForm(form))
    selection = form.tabs['general'].elements['select'].value
    
    if not selection:
        q.gui.dialog.showMessageBox(message = NO_ACTIVITIES_SELECTED,
                                    title = NO_ACTIVITIES,
                                    msgboxButtons = 'OK',
                                    msgboxIcon = 'Error')
    
    for s in selection:
        result = callCloudAPI(p.api, s)
        
def match(q, i, params, tags):
    return True