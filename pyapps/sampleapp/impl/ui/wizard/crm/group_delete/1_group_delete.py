MSG_DELETE = 'Warning! You are about to delete the group %s'
MSG_DELETE_CONFIRM = 'Are you sure you want to delete this group?'

def callCloudAPI(api, groupguid):
    result = api.action.crm.group.delete(groupguid)['result']    
    return result


def main(q, i, p, params, tags):
    
    group = p.api.action.crm.group.getObject(params['groupguid'], executionparams={'description': 'Retrieving lead information'})
    q.gui.dialog.message(MSG_DELETE% str(group))
    answer = q.gui.dialog.askYesNo(MSG_DELETE_CONFIRM, False)

    if answer == 'CANCEL':
		return
	
    result = callCloudAPI(p.api, params['groupguid'])
    params['result'] = result

def match(q, i, p, params, tags):
	return True
