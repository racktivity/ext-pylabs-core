__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    locationguid = params["locationguid"]
    location = p.api.model.racktivity.location.get(locationguid)
    from rootobjectaction_lib import rootobjectaction_find
    datacenters = rootobjectaction_find.datacenter_find(locationguid=locationguid)
    for datacenterguid in datacenters:
        p.api.action.racktivity.datacenter.delete(datacenterguid, request = params["request"])
    params['result'] = {'returncode': p.api.model.racktivity.location.delete(locationguid)}
    
    q.logger.log('Deleting policies linked to this location', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=locationguid)
    if policyguids:
        policyguid = policyguids[0]
        p.api.model.racktivity.policy.delete(policyguid)

    mtypes = ('current', 'voltage', 'frequency', 'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (locationguid, type))

    p.api.actor.racktivity.graphdatabase.destroyStores(databasenames)

def match(q, i, params, tags):
    return True
