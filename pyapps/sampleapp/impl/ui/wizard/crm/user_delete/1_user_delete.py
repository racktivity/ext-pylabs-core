MSG_DELETE = 'Warning! You are about to delete the user %s'
MSG_DELETE_CONFIRM = 'Are you sure you want to delete this user?'

def callCloudAPI(api, userguid):
    result = api.action.crm.user.delete(userguid)['result']    
    return result


def main(q, i, p, params, tags):
    
    user = p.api.action.crm.user.getObject(params['userguid'], executionparams={'description': 'Retrieving lead information'})
    q.gui.dialog.message(MSG_DELETE% str(user))
    answer = q.gui.dialog.askYesNo(MSG_DELETE_CONFIRM, False)

    if answer == 'CANCEL':
		return
	
    result = callCloudAPI(p.api, params['userguid'])
    params['result'] = result

def match(q, i, p, params, tags):
	return True
