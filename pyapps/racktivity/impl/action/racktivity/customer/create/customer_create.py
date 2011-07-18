__author__ = 'racktivity'
__tags__ ='customer', 'create'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    customer = q.drp.customer.new()
    customer.status = str(q.enumerators.customerstatustype.CONFIGURED)
    
    fields = ('description', 'address', 'city', 'country', 'name', 'tags')
    
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(customer, key, value)
    acl = customer.acl.new()
    customer.acl = acl
    q.drp.customer.save(customer)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(customer.guid, 'customer', params['request']['username'])

    params['result'] = {'returncode':True, 'customerguid': customer.guid}
    
def match(q, i, params, tags):
    return True
