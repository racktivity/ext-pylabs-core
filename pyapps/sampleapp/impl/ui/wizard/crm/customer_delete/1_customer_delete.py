MSG_DELETE = 'Warning! You\'re about to delete the customer <%s>'
MSG_DELETE_CONFIRM = 'Are you sure you want to delete this customer?'

def callCloudAPI(api, customerguid):
    result = api.action.crm.customer.delete(customerguid)['result']    
    return result


def main(q, i, p, params, tags):
    customer = p.api.action.crm.customer.getObject(params['customerguid'], executionparams={'description': 'Retrieving customer information'})
    q.gui.dialog.message(MSG_DELETE%customer.name)
    answer = q.gui.dialog.askYesNo(MSG_DELETE_CONFIRM, False)

    if answer == 'CANCEL':
        return
	
    result = callCloudAPI(p.api, customer.guid)
    params['result'] = result
