__author__ = 'incubaid'

def main(q, i, p, params, tags):
    permission = p.api.model.crm.permission.new()
    permission.name = params['name']
    permission.uri = params['uri']
    p.api.model.crm.permission.save(permission)
    params['result'] = permission.guid
    
def match(q, i, p, params, tags):
	return True