__author__ = 'racktivity'
__tags__ = 'feed', 'create'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find
import time

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0
    
CO2EMISSIONS = {'COAL':800.0,
                'GAS':430.0,
                'GENERIC':4.0,
                'GENERIC_GREEN':4.0,
                'NUCLEAR':6.0,
                'SOLAR':60.0,
                'WIND':3.0}

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #Check if another feed with the same name already exist
    datacenterguid = params['datacenterguid']
    if exists('view_feed_list', q.drp.feed, "name", params['name']):
        raise ValueError("Feed with the same name already exists")
    
    if datacenterguid and not exists('view_datacenter_list', q.drp.datacenter, "guid", datacenterguid):
        raise ValueError("Datacenter with guid %s doesn't exist"%params['datacenterguid'])
    
    feed = q.drp.feed.new()
    
    fields = ('name', 'datacenterguid', 'description', 'productiontype', 'system', 'tags')
    fieldsmap = {'productiontype': 'feedproductiontype'}
    
    objectfields = ('feedconnectors')
    
    for field in fields:
        fieldk = fieldsmap.get(field, field)
        if fieldk in params and params[fieldk]:
            setattr(feed, field, params[fieldk])
    
    for field in objectfields:
        fieldk = fieldsmap.get(field, field)
        if fieldk in params and params[fieldk]:
            value = params[fieldk]
            objlist = getattr(feed, field)
            for objectdata in value:
                obj = objlist.new()
                for k, v in objectdata.iteritems():
                    setattr(obj, k, v)
                objlist.append(obj)
     
    co2factor = params['co2emission']
    co2factor = float(co2factor) if co2factor != None else CO2EMISSIONS.get(str(params['feedproductiontype']), 0.0)
    feed.co2emission["%d" % time.time()] = co2factor
    acl = feed.acl.new()
    feed.acl = acl
    q.drp.feed.save(feed)
    
    if params['datacenterguid']:
        dcguid = params['datacenterguid']
        for guid in rootobjectaction_find.feed_find(datacenterguid=dcguid):
            if guid != feed.guid:
                wrongfeed = q.drp.feed.get(guid)
                wrongfeed.datacenterguid = ''
                q.drp.feed.save(wrongfeed)
                
    import racktivityui.uigenerator.feed
    racktivityui.uigenerator.feed.create(feed.guid)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(feed.guid, 'feed', params['request']['username'])

    params['result'] = {'returncode':True, 'feedguid': feed.guid}

def match(q, i, params, tags):
    return True

