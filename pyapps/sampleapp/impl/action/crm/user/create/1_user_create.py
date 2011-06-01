__author__ = 'incubaid'

def main(q, i, p, params, tags):
    user = p.api.model.crm.user.new()
    user.password = params['password']
    user.name = params['name']
    user.groups = params['groups']
    p.api.model.crm.user.save(user)
    params['result'] = user.guid
    
def match(q, i, p, params, tags):
	return True