__author__ = 'racktivity'
from logger import logger


def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    room = p.api.model.racktivity.room.get(params['roomguid'])
    q.logger.log('Updating model properties of room %s' % params['roomguid'], 3)
    fields = ('name', 'description', 'datacenterguid', 'floorguid', 'alias', 'tags')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(room, key, value)
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.room.save(room)
    
    params['result'] = {'returncode': True,
                        'roomguid': room.guid}

    #import racktivityui.uigenerator.room
    #import racktivityui.uigenerator.floor
    
    #racktivityui.uigenerator.room.update(room.guid)
    #if room.floor:
        #racktivityui.uigenerator.floor.update(room.floor)


def match(q, i, params, tags):
    return True
