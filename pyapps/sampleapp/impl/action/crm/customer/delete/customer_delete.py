__tags__ = 'customer','delete'
__author__ = 'incubaid'

def main(q, i, p, params, tags):
    p.api.model.crm.customer.delete(params['customerguid'])
    params['result'] = True
    
def match(q, i, p, params, tags):
	return True