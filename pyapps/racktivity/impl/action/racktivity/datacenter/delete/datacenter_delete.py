__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    datacenterguid = params['datacenterguid']
    datacenter = p.api.model.racktivity.datacenter.get(datacenterguid)
    from rootobjectaction_lib import rootobjectaction_find
    floors = rootobjectaction_find.floor_find(datacenterguid=datacenterguid)
    for floorguid in floors:
        p.api.action.racktivity.floor.delete(floorguid, request = params["request"])

    #Disconnects all the feed connectors, and set the Data center GUID to None
    feedguids = rootobjectaction_find.feed_find(datacenterguid=datacenterguid)
    feed = None
    if feedguids:
        feed = p.api.model.racktivity.feed.get(feedguids[0])
        if feed:
            for feedConnector in feed.feedconnectors:
                p.api.action.racktivity.feed.deleteConnector(feed.guid, feedConnector.name)
            feed.datacenterguid = None
            p.api.model.racktivity.feed.save(feed)

    params['result'] = {'returncode': p.api.model.racktivity.datacenter.delete(datacenterguid)}


    #Delete the policy linked to this datacenter
    q.logger.log('Deleting policies linked to this datacenter', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=datacenterguid)
    for policyguid in  policyguids:
        p.api.model.racktivity.policy.delete(policyguid)

    mtypes = ('current', 'voltage', 'frequency', 'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (datacenterguid, type))

    q.actions.actor.graphdatabase.destroyStores(databasenames)

def match(q, i, params, tags):
    return True

