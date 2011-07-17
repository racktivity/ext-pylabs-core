__author__ = 'racktivity'
__tags__ = 'row', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    rowguid = params["rowguid"]
    row = q.drp.row.get(rowguid)
    
    for rackguid in row.racks:
        q.actions.rootobject.rack.delete(rackguid, request = params["request"])
        
    params['result'] = {'returncode': q.drp.row.delete(rowguid)}

    
    #Delete the policy linked to this roe
    q.logger.log('Deleting policies linked to this row', 3)
    from rootobjectaction_lib import rootobjectaction_find
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=rowguid)
    for policyguid in  policyguids:
        q.drp.policy.delete(policyguid)

    import racktivityui.uigenerator
    racktivityui.uigenerator.deletePage(rowguid)
    
    import racktivityui.uigenerator.pod
    racktivityui.uigenerator.pod.update(row.pod)
    
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
        databasenames.append('%s_%s' % (rowguid, type))

    q.actions.actor.graphdatabase.destroyStores(url, databasenames)

def match(q, i, params, tags):
    return True
