__author__ = 'racktivity'
__tags__ = 'datacenter', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    datacenterguid = params['datacenterguid']
    datacenter = q.drp.datacenter.get(datacenterguid)
    from rootobjectaction_lib import rootobjectaction_find
    floors = rootobjectaction_find.floor_find(datacenterguid=datacenterguid)
    for floorguid in floors:
        q.actions.rootobject.floor.delete(floorguid, request = params["request"])

    #Disconnects all the feed connectors, and set the Data center GUID to None
    feedguids = rootobjectaction_find.feed_find(datacenterguid=datacenterguid)
    feed = None
    if feedguids:
        feed = q.drp.feed.get(feedguids[0])
        if feed:
            for feedConnector in feed.feedconnectors:
                q.actions.rootobject.feed.deleteConnector(feed.guid, feedConnector.name)
            feed.datacenterguid = None
            q.drp.feed.save(feed)

    params['result'] = {'returncode': q.drp.datacenter.delete(datacenterguid)}
    
    import racktivityui.uigenerator
    import racktivityui.uigenerator.campus
    racktivityui.uigenerator.campus.update(datacenter.locationguid)
    
    racktivityui.uigenerator.deletePage(datacenterguid)

    #Delete the policy linked to this datacenter
    q.logger.log('Deleting policies linked to this datacenter', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=datacenterguid)
    for policyguid in  policyguids:
        q.drp.policy.delete(policyguid)

    #Delete RRD databases on this datacenter
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
        databasenames.append('%s_%s' % (datacenterguid, type))
    
    q.actions.actor.graphdatabase.destroyStores(url, databasenames)

def match(q, i, params, tags):
    return True

