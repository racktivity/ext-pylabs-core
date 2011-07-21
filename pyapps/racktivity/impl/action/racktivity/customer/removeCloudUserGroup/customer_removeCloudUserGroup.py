__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    customer = p.api.model.racktivity.customer.get(params['customerguid'])
    if params['cloudusergroupguid'] in customer.cloudusergroups:
        customer.cloudusergroups.remove(params['cloudusergroupguid'])
    p.api.model.racktivity.customer.save(customer)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True

