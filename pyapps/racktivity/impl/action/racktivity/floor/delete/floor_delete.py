__author__ = 'racktivity'
__tags__ = 'floor', 'delete'
from logger import logger

from rootobjectaction_lib import rootobjectaction_find

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    floorguid = params['floorguid']
    q.logger.log('Deleting floor %s' % floorguid, 3)
    filterObject = q.drp.rack.getFilterObject()
    filterObject.add('view_rack_list', 'floorguid', floorguid)
    for roomguid in rootobjectaction_find.room_find(floor=floorguid):
        q.actions.rootobject.room.delete(roomguid, request = params["request"])
    
    for rackguid in rootobjectaction_find.rack_find(floor=floorguid):
        q.actions.rootobject.rack.delete(rackguid, request = params["request"])
        
    datacenterguid = q.drp.floor.get(floorguid).datacenterguid
    params['result'] = {'returncode': q.drp.floor.delete(floorguid)}

    #Update UI Pages
    import racktivityui.uigenerator.datacenter
    import racktivityui.uigenerator

    racktivityui.uigenerator.deletePage(floorguid)
    racktivityui.uigenerator.datacenter.update(datacenterguid)

    #Delete the policy linked to this floor
    q.logger.log('Deleting policies linked to this floor', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=floorguid)
    if policyguids:
        policyguid = policyguids[0]
        q.drp.policy.delete(policyguid)

    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name
    
    mtypes = ('current', 'voltage', 'frequency', 'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (floorguid, type))
    
    q.actions.actor.graphdatabase.destroyStores(url, databasenames)

def match(q, i, params, tags):
    return True