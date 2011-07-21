__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    customer = p.api.model.racktivity.customer.get(params['customerguid'])
    membercloudusergroup = params['cloudusergroupguid']
    customer.cloudusergroups.append(membercloudusergroup)
    p.api.model.racktivity.customer.save(customer)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True

