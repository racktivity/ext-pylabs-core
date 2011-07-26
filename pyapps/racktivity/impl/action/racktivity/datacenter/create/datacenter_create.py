__author__ = 'racktivity'
__priority__= 3
from logger import logger

from rootobjectaction_lib import rootobjectaction_find

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0
    
def main(q, i, p, params, tags):
    #logger.log_tasklet(("datacenter", "create"), params)
    params['result'] = {'returncode':False}
    keys = ('name', 'description', 'locationguid', 'clouduserguid', 'tags')
    
    #Check if another datacenter with the same name already exist
    if exists('racktivity_view_datacenter_list', p.api.model.racktivity.datacenter, "name", params['name']):
        raise ValueError("DataCenter with the same name already exists")
    #locationguid is valid?
    if not exists('racktivity_view_location_list', p.api.model.racktivity.location, "guid", params['locationguid']):
        raise ValueError("Location with guid %s doesn't exist"%params['locationguid'])
    #if clouduserguid is set, make sure its valid
    if params['clouduserguid'] and not exists('racktivity_view_clouduser_list', p.api.model.racktivity.clouduser, "guid", params['clouduserguid']):
        raise ValueError("clouduser with guid %s doesn't exist"%params['clouduserguid'])
    
    datacenter = p.api.model.racktivity.datacenter.new()
    for key, value in params.iteritems():
        if key in keys and value:
            setattr(datacenter, key, value)
    
    coordinates = datacenter.coordinates.new()
    datacenter.coordinates = coordinates
    
    if params['coordinatesinfo']:
        coordinatesinfo = params['coordinatesinfo']
        coordinates.latitude = float(coordinatesinfo['latitude'])
        coordinates.longitude = float(coordinatesinfo['longitude'])

    p.api.model.racktivity.datacenter.save(datacenter)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(datacenter.guid, 'datacenter', params['request']['username'])

    params['result'] = {'returncode': True,
                        'datacenterguid': datacenter.guid}

    q.logger.log('Creating a policy for datacenter %s' % datacenter.name, 3)
    
    p.api.action.racktivity.policy.create('datacenter_monitor_%s' % datacenter.name, rootobjecttype='datacenter', rootobjectaction='monitor',
                                       rootobjectguid=datacenter.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"])

    datacenterguid = datacenter.guid
    stores = list()
    mtypes = ('current', 'voltage', 'frequency', 'activeenergy',
              'apparentenergy', 'powerfactor')
    for type in mtypes:
        stores.append('%s_%s' % (datacenterguid, type))
    p.api.actor.graphdatabase.createStores(stores)

def match(q, i, params, tags):
    return True

