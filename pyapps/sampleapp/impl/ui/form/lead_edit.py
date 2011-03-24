__tags__ = 'wizard','lead','create'
__author__ = 'incubaid'

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


def callCloudAPI(api, name, code, customer, source, type, amount, probability):
    result = api.crm.lead.create(name, code, customer, source, type, status, amount, probability)['result']    
    return result

def getCustomers(api):
    customers = dict([customer['guid'],customer['description']] for customer in p.api.crm.customer.list()['result'])
    return customers

def getTypes(api):
    leadTypes = api.crm.lead.listTypes()['result']
    return leadTypes

def getSources(api):
    leadSources = api.crm.lead.listSources()['result']
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
    tab_general.addChoice(name='customer', text = TAB_GENERAL_CUSTOMER, values = getCustomers(p.api), selectValue=lead.customerguid, helpText = TAB_GENERAL_CUSTOMER_HELPTEXT, optional = True)
    tab_general.addChoice(name='source', text = TAB_GENERAL_SOURCE, values = getSources(p.api), value=lead.source, helpText = TAB_GENERAL_SOURCE_HELPTEXT, optional = True)
    tab_general.addChoice(name='type', text = TAB_GENERAL_TYPE, values = getTypes(p.api), value=lead.type, helpText = TAB_GENERAL_TYPE_HELPTEXT, optional = True)
    tab_general.addInteger(name='amount', text = TAB_GENERAL_AMOUNT, minValue=0, value=lead.amount, helpText=TAB_GENERAL_AMOUNT_HELPTEXT)
    tab_general.addInteger(name='probability', text = TAB_GENERAL_PROBABILITY, minValue=0, maxValue=100, value=lead.probability, helpText=TAB_GENERAL_PROBABILITY_HELPTEXT)    

    answer = q.gui.dialog.showMessageBox(message=MSGBOX_CREATE_CONFIRMATION,
                                         title=MSGBOX_CREATE_CONFIRMATION_TITLE,
                                         msgboxButtons='OKCancel',
                                         msgboxIcon='Question',
                                         defaultButton='OK')

    if answer == 'CANCEL':
        return

    result = callCloudAPI(p.api,
                          tab_general.elements['name'].value,
                          tab_general.elements['code'].value,
                          tab_general.elements['customer'].value,
                          tab_general.elements['source'].value,
                          tab_general.elements['type'].value,
                          tab_general.elements['amount'].value,
                          tab_general.elements['probability'].value)

def match(q, i, p, params, tags):
    return True
