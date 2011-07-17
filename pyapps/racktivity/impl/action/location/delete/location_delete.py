__author__ = 'racktivity'
__tags__ = 'location', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    locationguid = params["locationguid"]
    location = q.drp.location.get(locationguid)
    from rootobjectaction_lib import rootobjectaction_find
    datacenters = rootobjectaction_find.datacenter_find(locationguid=locationguid)
    for datacenterguid in datacenters:
        q.actions.rootobject.datacenter.delete(datacenterguid, request = params["request"])
    params['result'] = {'returncode': q.drp.location.delete(locationguid)}
    
    enterpriseguid = rootobjectaction_find.enterprise_find()[0]
    enterprise = q.drp.enterprise.get(enterpriseguid)
    if location.guid in enterprise.campuses:
        enterprise.campuses.remove(location.guid)
        q.drp.enterprise.save(enterprise)
    
    import racktivityui.uigenerator
    import racktivityui.uigenerator.enterprise
    racktivityui.uigenerator.deletePage(location.guid)
    racktivityui.uigenerator.enterprise.update()
    
    q.logger.log('Deleting policies linked to this location', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=locationguid)
    if policyguids:
        policyguid = policyguids[0]
        q.drp.policy.delete(policyguid)

    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name
    
    mtypes = ('current', 'voltage', 'frequency', 'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (locationguid, type))
    
    q.actions.actor.graphdatabase.destroyStores(url, databasenames)


def match(q, i, params, tags):
    return True
