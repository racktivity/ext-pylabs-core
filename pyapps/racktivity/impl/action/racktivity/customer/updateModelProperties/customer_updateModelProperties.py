__author__ = 'racktivity'
__tags__ = 'customer', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating customer properties in the model', 3)
    customer = q.drp.customer.get(params['customerguid'])
    
    paramKeys = ('name','description','address','city','country',
                 'retentionpolicyguid', 'tags')
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(customer, paramKey, params[paramKey])
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, paramKeys)
        q.drp.customer.save(customer)
    
    params['result'] = {'returncode':True, 'customerguid': customer.guid}

def match(q, i, params, tags):
    return True

