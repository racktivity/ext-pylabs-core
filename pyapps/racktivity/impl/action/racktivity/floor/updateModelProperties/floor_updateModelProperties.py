__author__ = 'racktivity'
__tags__ = 'floor', 'updateModelProperties'
from logger import logger


def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    floor = q.drp.floor.get(params['floorguid'])
    q.logger.log('Updating model properties of floor %s' % params['floorguid'], 3)
    fields = ('name', 'description', 'datacenterguid', 'floor', 'alias', 'tags')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(floor, key, value)
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, fields)
        q.drp.floor.save(floor)
    
    params['result'] = {'returncode': True,
                        'floorguid': floor.guid}

    import racktivityui.uigenerator.floor
    import racktivityui.uigenerator.datacenter
    
    racktivityui.uigenerator.floor.update(floor.guid)
    racktivityui.uigenerator.datacenter.update(floor.datacenterguid)


def match(q, i, params, tags):
    return True