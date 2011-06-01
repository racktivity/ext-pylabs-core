MSG_DELETE = 'Warning! You are about to delete the permission %s'
MSG_DELETE_CONFIRM = 'Are you sure you want to delete this permission?'

def callCloudAPI(api, permissionguid):
    result = api.action.crm.permission.delete(permissionguid)['result']    
    return result


def main(q, i, p, params, tags):
    
    permission = p.api.action.crm.permission.getObject(params['permissionguid'], executionparams={'description': 'Retrieving lead information'})
    q.gui.dialog.message(MSG_DELETE% str(permission))
    answer = q.gui.dialog.askYesNo(MSG_DELETE_CONFIRM, False)

    if answer == 'CANCEL':
		return
	
    result = callCloudAPI(p.api, params['permissionguid'])
    params['result'] = result

def match(q, i, p, params, tags):
	return True
