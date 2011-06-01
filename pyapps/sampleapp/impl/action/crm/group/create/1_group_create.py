__author__ = 'incubaid'

def main(q, i, p, params, tags):
    group = p.api.model.crm.group.new()
    group.name = params['name']
    group.permissions = params['permissions']
    p.api.model.crm.group.save(group)
    params['result'] = group.guid
    
def match(q, i, p, params, tags):
	return True