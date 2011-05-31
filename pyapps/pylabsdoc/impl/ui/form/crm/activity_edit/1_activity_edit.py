from datetime import datetime
import time
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
    types = q.enumerators.activitytype._pm_enumeration_items
    for key in types:
        types[key] = str(types[key])
    return types

def getStatus(q):
    status = q.enumerators.activitystatus._pm_enumeration_items
    for key in status:
        status[key] = str(status[key])
    return status

def getPriority(q):
    priority = q.enumerators.activitypriority._pm_enumeration_items
    for key in priority:
        priority[key] = str(priority[key])    
    return priority

        
def main(q, i, p, params, tags):
    cloudAPI = p.api
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
    type = getType(q)
    tab_general.addDropDown(name = 'type',
                            text = TAB_GENERAL_TYPE,
                            values = type,
                            selectedValue = str(activity.type))
    
    statuses = getStatus(q)
    tab_general.addDropDown(name = 'status',
                            text = TAB_GENERAL_STATUS,
                            values = statuses,
                            selectedValue = str(activity.status)
                            )
    
    priorities = getPriority(q)
    tab_general.addDropDown(name = 'priority',
                            text = TAB_GENERAL_PRIORITY,
                            values = priorities,
                            selectedValue = str(activity.priority),
                            )
    
    customers = getCustomer(q, cloudAPI)
    tab_general.addDropDown(name = 'customer',
                            text = TAB_GENERAL_CUSTOMER,
                            values = customers,
                            selectedValue =activity.customerguid)
    
    leads = getLead(q, cloudAPI)
    tab_general.addDropDown(name = 'lead',
                            text = TAB_GENERAL_LEAD,
                            values= leads ,
                            selectedValue = activity.leadguid)
    
    tab_general.addDateTime(name = 'starttime',
                            question = TAB_GENERAL_STARTTIME,
                            selectedValue = time.mktime(activity.starttime.timetuple()))
    
    tab_general.addDateTime(name = 'endtime',
                            question = TAB_GENERAL_ENDTIME,
                            selectedValue = time.mktime(activity.endtime.timetuple()))
                            
    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']

    result = p.api.action.crm.activity.update(
                          params['activityguid'],
                          tab_general.elements['name'].value,
                          tab_general.elements['description'].value,
                          tab_general.elements['location'].value,
                          tab_general.elements['type'].value,
                          tab_general.elements['priority'].value,
                          tab_general.elements['status'].value,
                          tab_general.elements['customer'].value,
                          tab_general.elements['lead'].value,
                          tab_general.elements['starttime'].value,
                          tab_general.elements['endtime'].value)

    params['result'] = result
       
       
    def match(q, i, params, tags):
        return True
