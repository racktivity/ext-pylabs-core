__author__ = 'racktivity'
__priority__ = 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    q.logger.log('Creating new room', 4)
    fields = ('name', 'description', 'datacenterguid', 'floorguid', 'alias', 'tags')
    #Do some checks
    if rootobjectaction_find.find('room', name = params['name']):
        raise ValueError("Room with name %s already exists"%params['name'])
    if not params['datacenterguid'] or not rootobjectaction_find.find('datacenter', guid = params['datacenterguid']):
        raise ValueError("Invalid datacenterguid %s"%params['datacenterguid'])
    
    room = p.api.model.racktivity.room.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(room, key, value)

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
