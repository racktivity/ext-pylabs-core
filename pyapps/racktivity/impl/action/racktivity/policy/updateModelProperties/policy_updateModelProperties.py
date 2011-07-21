__author__ = 'racktivity'
__priority__ = 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Update policy properties in the model', 3)
    fields = ('name', 'description', 'lastrun', 'policyparams', 'interval', 'runbetween', 'runnotbetween', 'tags')
    logged_fields = ('name', 'description', 'policyparams', 'interval', 'runbetween', 'runnotbetween', 'tags')
    policy = p.api.model.racktivity.policy.get(params['policyguid'])
    changed = False
    
    for key, value in params.iteritems():
        if key not in fields or (value is None):
            continue
        setattr(policy, key, value)
        changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, logged_fields)
        p.api.model.racktivity.policy.save(policy)
    params['result'] = {'returncode':True, 'policyguid': policy.guid}

def match(q,i,params,tags):
    return True
