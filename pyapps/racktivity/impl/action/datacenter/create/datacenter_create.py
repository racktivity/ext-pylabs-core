__author__ = 'racktivity'
__tags__ = 'datacenter', 'create'
__priority__= 3
from logger import logger

from rootobjectaction_lib import rootobjectaction_find

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0
    
def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    keys = ('name', 'description', 'locationguid', 'clouduserguid', 'tags')
    
    #Check if another datacenter with the same name already exist
    if exists('view_datacenter_list', q.drp.datacenter, "name", params['name']):
        raise ValueError("DataCenter with the same name already exists")
    #locationguid is valid?
    if not exists('view_location_list', q.drp.location, "guid", params['locationguid']):
        raise ValueError("Location with guid %s doesn't exist"%params['locationguid'])
    #if clouduserguid is set, make sure its valid
    if params['clouduserguid'] and not exists('view_clouduser_list', q.drp.clouduser, "guid", params['clouduserguid']):
        raise ValueError("clouduser with guid %s doesn't exist"%params['clouduserguid'])
    
    datacenter = q.drp.datacenter.new()
    for key, value in params.iteritems():
        if key in keys and value:
            setattr(datacenter, key, value)
    
    coordinates = datacenter.coordinates.new()
    datacenter.coordinates = coordinates
    
    if params['coordinatesinfo']:
        coordinatesinfo = params['coordinatesinfo']
        coordinates.latitude = float(coordinatesinfo['latitude'])
        coordinates.longitude = float(coordinatesinfo['longitude'])
    acl = datacenter.acl.new()
    datacenter.acl = acl
    q.drp.datacenter.save(datacenter)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(datacenter.guid, 'datacenter', params['request']['username'])

    params['result'] = {'returncode': True,
                        'datacenterguid': datacenter.guid}

    q.logger.log('Creating a policy for datacenter %s' % datacenter.name, 3)
    
    q.actions.rootobject.policy.create('datacenter_monitor_%s' % datacenter.name, rootobjecttype='datacenter', rootobjectaction='monitor',
                                       rootobjectguid=datacenter.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"])
    
    
    import racktivityui.uigenerator.datacenter
    racktivityui.uigenerator.datacenter.create(datacenter.guid, datacenter.locationguid)
    import racktivityui.uigenerator.campus
    racktivityui.uigenerator.campus.update(datacenter.locationguid)

    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name

    datacenterguid = datacenter.guid
    stores = list()
    mtypes = ('current', 'voltage', 'frequency', 'activeenergy',
              'apparentenergy', 'powerfactor')
    for type in mtypes:
        stores.append('%s_%s' % (datacenterguid, type))
    
    q.actions.actor.graphdatabase.createStores(url, stores)

def match(q, i, params, tags):
    return True

