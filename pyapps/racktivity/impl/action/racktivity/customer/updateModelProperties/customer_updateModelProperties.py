__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating customer properties in the model', 3)
    customer = p.api.model.racktivity.customer.get(params['customerguid'])
    
    paramKeys = ('name','description','address','city','country',
                 'retentionpolicyguid', 'tags')
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(customer, paramKey, params[paramKey])
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, paramKeys)
        p.api.model.racktivity.customer.save(customer)
    
    params['result'] = {'returncode':True, 'customerguid': customer.guid}

def match(q, i, params, tags):
    return True

