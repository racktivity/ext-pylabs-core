__author__ = 'racktivity'
from logger import logger

from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    floorguid = params['floorguid']
    q.logger.log('Deleting floor %s' % floorguid, 3)
    filterObject = p.api.model.racktivity.rack.getFilterObject()
    filterObject.add('racktivity_view_rack_list', 'floorguid', floorguid)
    for roomguid in rootobjectaction_find.room_find(floor=floorguid):
        p.api.action.racktivity.room.delete(roomguid, request = params["request"])
    
    for rackguid in rootobjectaction_find.rack_find(floor=floorguid):
        p.api.action.racktivity.rack.delete(rackguid, request = params["request"])
        
    datacenterguid = p.api.model.racktivity.floor.get(floorguid).datacenterguid
    params['result'] = {'returncode': p.api.model.racktivity.floor.delete(floorguid)}

    #Delete the policy linked to this floor
    q.logger.log('Deleting policies linked to this floor', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=floorguid)
    if policyguids:
        policyguid = policyguids[0]
        p.api.model.racktivity.policy.delete(policyguid)

    #Delete the data stores
    mtypes = ('current', 'voltage', 'frequency', 'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (floorguid, type))
    
    p.api.actor.graphdatabase.destroyStores(databasenames)

def match(q, i, params, tags):
    return True
