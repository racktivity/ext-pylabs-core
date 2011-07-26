__author__ = 'racktivity'
__priority__ = 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    fields = ('name', 'rootobjecttype', 'rootobjectaction', 'rootobjectguid', \
              'interval', 'runbetween', 'runnotbetween', 'policyparams', 
              'description', 'tags')
    filterobj = p.api.model.racktivity.policy.getFilterObject()
    filterobj.add('racktivity_view_policy_list', 'name', params['name'])
    policyexists = p.api.model.racktivity.policy.find(filterobj)
    if policyexists:
        raise ValueError('Policy with name "%s" already exists' % params['name'])

    policy = p.api.model.racktivity.policy.new()
    for key, value in params.iteritems():
        if key == 'runbetween' and not value:
            value = '[("00:00", "23:59")]'
        if key in fields and value:
            if key == 'interval':
                value = float(value)
            setattr(policy, key, value)

    p.api.model.racktivity.policy.save(policy)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(policy.guid, 'policy', params['request']['username'])

    params['result'] = {'returncode':True, 'policyguid':policy.guid}

def match(q,i,params,tags):
    return True
