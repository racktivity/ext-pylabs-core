__author__ = 'racktivity'
__tags__ = 'room', 'create'
__priority__ = 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    q.logger.log('Creating new room', 4)
    fields = ('name', 'description', 'datacenterguid', 'floor', 'alias', 'tags')
    #Do some checks
    if exists('view_room_list', q.drp.room, "name", params['name']):
        raise ValueError("Room with name %s already exists"%params['name'])
    if not exists('view_datacenter_list', q.drp.datacenter, "guid", params['datacenterguid']):
        raise ValueError("Invalid datacenterguid %s"%params['datacenterguid'])
    
    room = q.drp.room.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(room, key, value)
    acl = room.acl.new()
    room.acl = acl
    q.drp.room.save(room)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(room.guid, 'room', params['request']['username'])

    q.logger.log('Creating a policy for room %s' % room.name, 3)
    q.actions.rootobject.policy.create('room_%s' % room.name, rootobjecttype='room', rootobjectaction='monitor',
                                       rootobjectguid=room.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"]
                                       )

    #Generate UI page
    import racktivityui.uigenerator.floor
    import racktivityui.uigenerator.room

    racktivityui.uigenerator.room.create(room.guid, room.floor)
    racktivityui.uigenerator.floor.update(room.floor)

    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name

    roomguid = room.guid
    stores = list()
    mtypes = ('current', 'voltage', 'frequency', 'activeenergy',
              'apparentenergy', 'powerfactor')
    for type in mtypes:
        stores.append('%s_%s' % (roomguid, type))
    
    q.actions.actor.graphdatabase.createStores(url, stores)
    
    params['result'] = {'returncode': True,
                        'roomguid': room.guid}

def match(q, i, params, tags):
    return True