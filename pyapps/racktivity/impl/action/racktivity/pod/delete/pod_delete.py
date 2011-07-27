__author__ = 'racktivity'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode':False}
    podguid = params["podguid"]
    
    for rackguid in rootobjectaction_find.find("rack", podguid = podguid):
        p.api.action.racktivity.rack.delete(rackguid, request = params["request"])
    
    for rowguid in rootobjectaction_find.find("row", podguid = podguid):
        p.api.action.racktivity.row.delete(rowguid, request = params["request"])
    
    params['result'] = {'returncode': p.api.model.racktivity.pod.delete(podguid)}

    #Delete the policy linked to this pod
    q.logger.log('Deleting policies linked to this pod', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=podguid)
    for policyguid in  policyguids:
        p.api.model.racktivity.policy.delete(policyguid)

    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (podguid, type))
    
    p.api.actor.racktivity.graphdatabase.destroyStores(databasenames)

def match(q, i, params, tags):
    return True
