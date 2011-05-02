TAB_GENERAL_TITLE = 'General'
TAB_GENERAL_NAME = 'Name: '
TAB_GENERAL_CODE = 'Code: '
TAB_GENERAL_CUSTOMER_NAME = 'Customer: '
TAB_GENERAL_CUSTOMER_GUID = 'Customer GUID: '
TAB_GENERAL_SOURCE = 'Source: '
TAB_GENERAL_TYPE = 'Type: '
TAB_GENERAL_STATUS = 'Status: '
TAB_GENERAL_AMOUNT = 'Amount: '
TAB_GENERAL_PROBABILITY = 'Probability: '


TAB_GENERAL_NAME_HELPTEXT = 'Please provide the lead\'s name'
TAB_GENERAL_CODE_HELPTEXT = 'Please provide the lead\'s code'
TAB_GENERAL_CUSTOMER_HELPTEXT = 'Please provide the lead\'s related customer'
TAB_GENERAL_SOURCE_HELPTEXT = 'Please provide the lead\'s source'
TAB_GENERAL_TYPE_HELPTEXT = 'Please provide the lead\'s type'
TAB_GENERAL_STATUS_HELPTEXT = 'Please provide the lead\'s status'
TAB_GENERAL_AMOUNT_HELPTEXT = 'Please provide the lead\'s amount'
TAB_GENERAL_PROBABILITY_HELPTEXT = 'Please provide the lead\'s probability'


MSGBOX_CREATE_CONFIRMATION = "Create this new lead?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "lead creation"

MSGBOX_lead_CREATE_FAILED = "Failed to create this new lead! Please contact your system administrator!"
MSGBOX_lead_CREATE_FAILED_TITLE = "lead creation failed"


def callCloudAPI(api, name, code, customer, source, type, status, amount, probability):
    result = api.action.crm.lead.create(name, code, customer, source, type, status, amount, probability)['result']    
    return result

#~ def getCustomers(api):
    #~ customers = dict([customer['guid'],customer['name']] for customer in api.action.crm.customer.list()['result'])
    #~ return customers

def getTypes(api):
    leadTypes_list = api.action.crm.lead.listTypes()['result']
    leadTypes = dict.fromkeys(leadTypes_list)
    for k in leadTypes.iterkeys():
        leadTypes[k] = k
    return leadTypes

def getStatuses(api):
    leadStatuses_list = api.action.crm.lead.listStatuses()['result']
    leadStatuses = dict.fromkeys(leadStatuses_list)
    for k in leadStatuses.iterkeys():
        leadStatuses[k] = k
    return leadStatuses

def getSources(api):
    #dict([customer['guid'],customer['name']] for customer in api.action.crm.customer.list()['result'])
    leadSources_list = api.action.crm.lead.listSources()['result']
    leadSources = dict.fromkeys(leadSources_list)
    for k in leadSources.iterkeys():
        leadSources[k] = k
    return leadSources

def main(q, i, p, params, tags):
    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)
    
    customerguid = params['customerguid']
    customer = p.api.action.crm.customer.getObject(customerguid)

    ###########################
    # General information tab #
    ###########################
    tab_general.addText(name='name', text = TAB_GENERAL_NAME, helpText = TAB_GENERAL_NAME_HELPTEXT)
    tab_general.addText(name='code', text = TAB_GENERAL_CODE, helpText = TAB_GENERAL_CODE_HELPTEXT)
    tab_general.addChoice(name='source', text = TAB_GENERAL_SOURCE, values = getSources(p.api), helpText = TAB_GENERAL_SOURCE_HELPTEXT, optional = True)
    tab_general.addChoice(name='type', text = TAB_GENERAL_TYPE, values = getTypes(p.api), helpText = TAB_GENERAL_TYPE_HELPTEXT, optional = True)
    tab_general.addChoice(name='status', text = TAB_GENERAL_STATUS, values=getStatuses(p.api), helpText = TAB_GENERAL_TYPE_HELPTEXT, optional=True)
    tab_general.addInteger(name='amount', text = TAB_GENERAL_AMOUNT, minValue=0, value=0, helpText=TAB_GENERAL_AMOUNT_HELPTEXT)
    tab_general.addInteger(name='probability', text = TAB_GENERAL_PROBABILITY, minValue=0, maxValue=100, value=50, helpText=TAB_GENERAL_PROBABILITY_HELPTEXT)

    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']
    
    result = callCloudAPI(p.api,
                          tab_general.elements['name'].value,
                          tab_general.elements['code'].value,
                          customer.guid,
                          tab_general.elements['source'].value,
                          tab_general.elements['type'].value,
                          tab_general.elements['status'].value,
                          float(tab_general.elements['amount'].value),
                          int(tab_general.elements['probability'].value))
    params['result'] = result
