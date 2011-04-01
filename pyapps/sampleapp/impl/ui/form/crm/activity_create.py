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

def getCustomers(q, api):
    customers = dict()
    result = api.action.crm.customer.list()['result']
    
    map(lambda x: customers.__setitem__(x['guid'], x['name']), result)
    return customers

def getLeads(q, api):
    leads = dict()
    result = api.action.crm.lead.list()['result']
    
    map(lambda x: leads.__setitem__(x['guid'], x['name']), result)
    return leads

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
    
    type = getType(q)
    status= getStatus(q)
    priority = getPriority(q)
    customers = getCustomers(q, p.api)
    leads = getLeads(q, p.api)
    
    form = q.gui.form.createForm()
    
    #alternative way
    #form.addTab('general',TAB_GENERAL_TITLE)
    #form.tabs['general'].addText blablabla
    
    tab_general = form.addTab('general', TAB_GENERAL_TITLE)
    
    #define fields of tab
    tab_general.addText(name = 'name',
                        text = TAB_GENERAL_NAME)
    
    tab_general.addText(name = 'description',
                        text = TAB_GENERAL_DESCRIPTION,
                        multiline = True)
    
    tab_general.addText(name = 'location',
                        text = TAB_GENERAL_LOCATION)
    
    tab_general.addDropDown(name = 'type',
                            text = TAB_GENERAL_TYPE,
                            values = type)
    
    tab_general.addDropDown(name = 'status',
                            text = TAB_GENERAL_STATUS,
                            values = status)
    
    tab_general.addDropDown(name = 'priority',
                            text = TAB_GENERAL_PRIORITY,
                            values = priority)
    
    tab_general.addDropDown(name = 'customer',
                            text = TAB_GENERAL_CUSTOMER,
                            values = customers,
                            selectedValue = 0)
    
    tab_general.addDropDown(name = 'lead',
                            text = TAB_GENERAL_LEAD,
                            values = leads,
                            selectedValue = 0)
    
    tab_general.addDateTime(name = 'starttime',
                            question = TAB_GENERAL_STARTTIME)
    
    tab_general.addDateTime(name = 'endtime',
                        question = TAB_GENERAL_ENDTIME)
    
    
    #below shows up when clicked button in tab after entering all values
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

    params['result'] = result
