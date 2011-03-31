__tags__ = 'wizard','lead','delete'
__author__ = 'incubaid'

MSG_DELETE = 'Warning! You\'re about to delete the lead <%s>'
MSG_DELETE_CONFIRM = 'Are you sure you want to delete this customer?'

def callCloudAPI(api, leadguid):
    result = api.crm.lead.delete(leadguid)['result']    
    return result


def main(q, i, p, params, tags):
    lead = p.api.action.crm.customer.getObject(params['leadguid'], executionparams={'description': 'Retrieving lead information'})
    q.gui.dialog.message(MSG_DELETE%lead.name)
    answer = q.gui.dialog.askYesNo(MSG_DELETE_CONFIRM, False)

    if answer == 'CANCEL':
		return
	
    result = callCloudAPI(p.api, lead.guid)

def match(q, i, p, params, tags):
	return True