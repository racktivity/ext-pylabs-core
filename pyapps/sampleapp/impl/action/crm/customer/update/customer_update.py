__tags__ = 'customer','update'
__author__ = 'incubaid'

def main(q, i, p, params, tags):
    customer = p.api.model.crm.customer.get(params['customerguid'])
    customer.name = params['name']
    customer.email = params['email']
    customer.login = params['login']
    customer.password = params['password']
    customer.address = params.get('address')
    customer.vat = params.get('vat')
    p.api.model.crm.customer.save(customer)
    params['result'] = True
    
def match(q, i, p, params, tags):
	return True