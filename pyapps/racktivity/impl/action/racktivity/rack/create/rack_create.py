__author__ = 'racktivity'
__tags__ = 'rack', 'create'
__priority__= 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    fields = ('name', 'racktype', 'description', 'roomguid', 'floor', 'corridor', 
              'position', 'height', 'tags')
    #Do some checks
    if exists('view_rack_list', q.drp.rack, "name", params['name']):
        raise ValueError("Rack with name %s already exists"%params['name'])
    
    roomguid = params.get('roomguid', '')
    floorguid = params.get('floor', '')
    if not roomguid and not floorguid:
        raise ValueError("Can't create a rack with no roomguid or floorguid, at least one is required")
    
    rack = q.drp.rack.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(rack, key, value)
    acl = rack.acl.new()
    rack.acl = acl
    q.drp.rack.save(rack)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(rack.guid, 'rack', params['request']['username'])

    q.logger.log('Creating a policy for rack %s' % rack.name, 3)
    q.actions.rootobject.policy.create('rack_%s' % rack.name, rootobjecttype='rack', rootobjectaction='monitor',
                                       rootobjectguid=rack.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"])

    if rack.roomguid:
        import racktivityui.uigenerator.room
        racktivityui.uigenerator.room.update(rack.roomguid)
        q.actions.rootobject.rack.uiCreatePageUnderParent(rack.guid, rack.roomguid)
    elif rack.floor:
        q.actions.rootobject.rack.uiCreatePageUnderParent(rack.guid, rack.floor)
        import racktivityui.uigenerator.floor
        racktivityui.uigenerator.floor.update(rack.floor)
    
    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name

    rackguid = rack.guid
    
    stores = list()
    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    for type in mtypes:
        stores.append('%s_%s' % (rackguid, type))
    
    q.actions.actor.graphdatabase.createStores(url, stores)
    
    params['result'] = {'returncode': True,
                        'rackguid': rack.guid}

def match(q, i, params, tags):
    return True
