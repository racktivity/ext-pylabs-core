__tags__ = 'wizard', 'activity', 'create'
__author__ = 'incubaid'

TAB_GENERAL_TITLE = 'Create Activity'
TAB_GENERAL_NAME = 'Activity name : '
TAB_GENERAL_DESCRIPTION = 'Activity description : '
TAB_GENERAL_LOCATION = 'Location : '
TAB_GENERAL_TYPE = 'Activity type : '
TAB_GENERAL_STATUS = 'Status : '
TAB_GENERAL_PRIORITY = 'Priority : '
TAB_GENERAL_CUSTOMER = 'Customer : '
TAB_GENERAL_LEAD = 'Lead : '
TAB_GENERAL_STARTTIME = 'Start time : '
TAB_GENERAL_ENDTIME = 'End time : '


MSGBOX_CONFIRMATION = 'Confirm activity?' 
MSGBOX_CONFIRMATION_TITLE = 'Confirm activity?'


def callCloudAPI(api, name, description, location, type, priority, status, customerguid, leadguid, starttime, endtime):
    result = api.crm.activity.create(name, description, location, type, priority, status, customerguid, leadguid, starttime, endtime)['result']    
    return result

def getCustomer(q, api):
    customers = dict()
    result = api.action.crm.customer.list()['result']
    
    map(lambda x: customers.__setitem__(x['guid'], x['name']), result)
    return customers

def getLead(q, api):
    lead = dict()
    result = api.action.crm.lead.list()['result']
    
    map(lambda x: lead.__setitem__(x['guid'], x['name']), result)
    return lead

def getType(q):
    type = q.enumerators.activitytype._pm_enumeration_items
    return type

def getStatus(q):
    status = q.enumerators.activitystatus._pm_enumeration_items
    return status

def getPriority(q):
    priority = q.enumerators.activitypriority._pm_enumeration_items
    return priority


def main(q, i, p, params, tags):
    
    cloudAPI = i.config.cloudApiConnection.find('main')
    cloudAPI.setCredentials(params['login'],params['password'])
    
    form = q.gui.form.createForm()
    tab_general = form.addTab('general', TAB_GENERAL_TITLE)
    
    activity = p.api.action.crm.activity.getObject(params['activityguid'], executionparams={'description': 'Retrieving activity information'})
    tab_general.addText(name = 'name',
                        text = TAB_GENERAL_NAME,
                        value = activity.name)
    
    tab_general.addText(name = 'description',
                        text = TAB_GENERAL_DESCRIPTION,
                        value = activity.description,
                        multiline = True)
    
    tab_general.addText(name = 'location',
                        text = TAB_GENERAL_LOCATION,
                        value = activity.location)
    
    tab_general.addDropDown(name = 'type',
                            text = TAB_GENERAL_TYPE,
                            value = activity.type,
                            values = type)
    
    tab_general.addDropDown(name = 'status',
                            text = TAB_GENERAL_STATUS,
                            value = activity.status,
                            values = status)
    
    tab_general.addDropDown(name = 'priority',
                            text = TAB_GENERAL_PRIORITY,
                            value = activity.priority,
                            values = priority)
    
    tab_general.addDropDown(name = 'customer',
                            text = TAB_GENERAL_CUSTOMER,
                            value = activity.customerguid,
                            values = customers,
                            selectedValue = 0)
    
    tab_general.addDropDown(name = 'lead',
                            text = TAB_GENERAL_LEAD,
                            value = activity.leadguid,
                            values = lead,
                            selectedValue = 0)
    
    tab_general.addDateTime(name = 'starttime',
                            question = TAB_GENERAL_STARTTIME,
                            value = activity.starttime)
    
    tab_general.addDateTime(name = 'endtime',
                            question = TAB_GENERAL_ENDTIME,
                            value = activity.endtime)
    
    answer = q.gui.dialog.showMessageBox(message = MSGBOX_CONFIRMATION,
                                         title = MSGBOX_CONFIRMATION_TITLE,
                                         msgboxButtons = 'YesNo',
                                         msgboxIcon = 'Question',
                                         defaultButton = 'Yes')
    
    if answer == 'No':
        return
    
    result = callCloudAPI(p.api,
                          tab_general.elements['name'].value,
                          tab_general.elements['description'].value,
                          tab_general.elements['location'].value,
                          tab_general.elements['type'].value,
                          tab_general.elements['status'].value,
                          tab_general.elements['priority'].value,
                          tab_general.elements['customer'].value,
                          tab_general.elements['lead'].value,
                          tab_general.elements['starttime'].value,
                          tab_general.elements['endtime'].value,)
       
       
    def match(q, i, params, tags):
        return True