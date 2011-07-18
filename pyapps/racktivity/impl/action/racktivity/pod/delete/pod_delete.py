__author__ = 'racktivity'
__tags__ = 'pod', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode':False}
    podguid = params["podguid"]
    pod = q.drp.pod.get(podguid)
    
    for rackguid in pod.racks:
        q.actions.rootobject.rack.delete(rackguid, request = params["request"])
    
    for rowguid in rootobjectaction_find.row_find(pod=podguid):
        q.actions.rootobject.row.delete(rowguid, request = params["request"])
        
    params['result'] = {'returncode': q.drp.pod.delete(podguid)}

    #Delete the policy linked to this pod
    q.logger.log('Deleting policies linked to this pod', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=podguid)
    for policyguid in  policyguids:
        q.drp.policy.delete(policyguid)

    import racktivityui.uigenerator
    racktivityui.uigenerator.deletePage(podguid)
    
    import racktivityui.uigenerator.room
    racktivityui.uigenerator.room.update(pod.room)
    
    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name
    
    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (podguid, type))
    
    q.actions.actor.graphdatabase.destroyStores(url, databasenames)

def match(q, i, params, tags):
    return True
