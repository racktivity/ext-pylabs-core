__author__ = 'racktivity'
__tags__ = 'room', 'delete'
from logger import logger

from rootobjectaction_lib import rootobjectaction_find

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    roomguid = params['roomguid']
    q.logger.log('Deleting room %s' % roomguid, 3)
    
    for podguid in rootobjectaction_find.pod_find(room=roomguid):
        q.actions.rootobject.pod.delete(podguid, request = params["request"])
    
    for rackguid in rootobjectaction_find.rack_find(roomguid=roomguid):
        q.actions.rootobject.rack.delete(rackguid, request = params["request"])
    
    floorguid = q.drp.room.get(roomguid).floor
    params['result'] = {'returncode': q.drp.room.delete(roomguid)}

    import racktivityui.uigenerator.floor
    import racktivityui.uigenerator

    racktivityui.uigenerator.deletePage(roomguid)
    if floorguid:
        racktivityui.uigenerator.floor.update(floorguid)

    #Delete the policy linked to this room
    q.logger.log('Deleting policies linked to this room', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=roomguid)
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
        databasenames.append('%s_%s' % (roomguid, type))
    
    q.actions.actor.graphdatabase.destroyStores(url, databasenames)

def match(q, i, params, tags):
    return True