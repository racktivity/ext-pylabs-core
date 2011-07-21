__author__ = 'racktivity'
__priority__ = 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    q.logger.log('Creating new room', 4)
    fields = ('name', 'description', 'datacenterguid', 'floor', 'alias', 'tags')
    #Do some checks
    if exists('racktivity_view_room_list', p.api.model.racktivity.room, "name", params['name']):
        raise ValueError("Room with name %s already exists"%params['name'])
    if not exists('racktivity_view_datacenter_list', p.api.model.racktivity.datacenter, "guid", params['datacenterguid']):
        raise ValueError("Invalid datacenterguid %s"%params['datacenterguid'])
    
    room = p.api.model.racktivity.room.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(room, key, value)
    acl = room.acl.new()
    room.acl = acl
    p.api.model.racktivity.room.save(room)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(room.guid, 'room', params['request']['username'])

    q.logger.log('Creating a policy for room %s' % room.name, 3)
    p.api.action.racktivity.policy.create('room_%s' % room.name, rootobjecttype='room', rootobjectaction='monitor',
                                       rootobjectguid=room.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"]
                                       )

    #Generate UI page
    #import racktivityui.uigenerator.floor
    #import racktivityui.uigenerator.room

    #racktivityui.uigenerator.room.create(room.guid, room.floor)
    #racktivityui.uigenerator.floor.update(room.floor)

    params['result'] = {'returncode': True,
                        'roomguid': room.guid}

def match(q, i, params, tags):
    return True
