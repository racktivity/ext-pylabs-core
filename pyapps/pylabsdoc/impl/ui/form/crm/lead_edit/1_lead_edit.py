TAB_GENERAL_TITLE = 'General'
TAB_GENERAL_NAME = 'Name: '
TAB_GENERAL_CODE = 'Code: '
TAB_GENERAL_CUSTOMER = 'Customer: '
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


MSGBOX_CREATE_CONFIRMATION = "Edit this lead?"
MSGBOX_CREATE_CONFIRMATION_TITLE = "lead update"

MSGBOX_lead_CREATE_FAILED = "Failed to update this lead! Please contact your system administrator!"
MSGBOX_lead_CREATE_FAILED_TITLE = "lead update failed"

def getCustomers(api):
    customers = dict([customer['guid'],customer['name']] for customer in api.action.crm.customer.list()['result'])
    return customers

def getTypes(api):
    leadTypes = dict([str(type),str(type)]for type in api.action.crm.lead.listTypes()['result'])
    return leadTypes

def getStatuses(api):
    leadStatuses = dict([str(status), str(status)] for status in api.action.crm.lead.listStatuses()['result'])
    return leadStatuses

def getSources(api):
    leadSources = dict([str(source), str(source)] for source in api.action.crm.lead.listSources()['result'])
    return leadSources

def main(q, i, p, params, tags):

    form = q.gui.form.createForm()
    tab_general  = form.addTab('general' , TAB_GENERAL_TITLE)

    ###########################
    # General information tab #
    ###########################
    lead = p.api.action.crm.lead.getObject(params['leadguid'], executionparams={'description': 'Retrieving lead information'})    
    tab_general.addText(name='name', text = TAB_GENERAL_NAME, value=lead.name, helpText = TAB_GENERAL_NAME_HELPTEXT)
    tab_general.addText(name='code', text = TAB_GENERAL_CODE, value=lead.code, helpText = TAB_GENERAL_CODE_HELPTEXT)
    tab_general.addDropDown(name='customer', text = TAB_GENERAL_CUSTOMER, values = getCustomers(p.api), selectedValue=lead.customerguid, helpText = TAB_GENERAL_CUSTOMER_HELPTEXT, optional = True)
    tab_general.addChoice(name='source', text = TAB_GENERAL_SOURCE, values = getSources(p.api), selectedValue=str(lead.source), helpText = TAB_GENERAL_SOURCE_HELPTEXT, optional = True)
    tab_general.addChoice(name='type', text = TAB_GENERAL_TYPE, values = getTypes(p.api), selectedValue=str(lead.type), helpText = TAB_GENERAL_TYPE_HELPTEXT, optional = True)
    tab_general.addChoice(name='status', text=TAB_GENERAL_STATUS, values=getStatuses(p.api), selectedValue=str(lead.status), helpText=TAB_GENERAL_TYPE_HELPTEXT, optional=True)
    tab_general.addInteger(name='amount', text = TAB_GENERAL_AMOUNT, minValue=0, value=lead.amount, helpText=TAB_GENERAL_AMOUNT_HELPTEXT)
    tab_general.addInteger(name='probability', text = TAB_GENERAL_PROBABILITY, minValue=0, maxValue=100, value=lead.probability, helpText=TAB_GENERAL_PROBABILITY_HELPTEXT)    

    form.loadForm(q.gui.dialog.askForm(form))
    tab_general = form.tabs['general']

    result = p.api.action.crm.lead.update(
                          params['leadguid'],
                          tab_general.elements['name'].value,
                          tab_general.elements['code'].value,
                          tab_general.elements['customer'].value,
                          tab_general.elements['source'].value,
                          tab_general.elements['type'].value,
                          tab_general.elements['status'].value,
                          float(tab_general.elements['amount'].value),
                          int(tab_general.elements['probability'].value))['result']
    params['result'] = result

def match(q, i, p, params, tags):
    return True
