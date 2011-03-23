__tags__ = 'customer','create'
__author__ = 'incubaid'

def main(q, i, p, params, tags):
    customer = p.api.model.crm.customer.new()
    customer.name = params['name']
    customer.email = params['email']
    customer.login = params['login']
    customer.password = params['password']
    customer.address = params.get('address')
    customer.vat = params.get('vat')
    p.api.model.crm.customer.save(customer)
    
def match(q, i, p, params, tags):
	return True