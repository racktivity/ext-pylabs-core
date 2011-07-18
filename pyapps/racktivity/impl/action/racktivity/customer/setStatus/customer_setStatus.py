__author__ = 'racktivity'
__tags__ ='customer', 'setStatus'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    customer = q.drp.customer.get(params['customerguid'])
    customer.status = str(params['status'])
    q.drp.customer.save(customer)
    params['result'] = {'returncode':True}
	
def match(q, i, params, tags):
    return True
