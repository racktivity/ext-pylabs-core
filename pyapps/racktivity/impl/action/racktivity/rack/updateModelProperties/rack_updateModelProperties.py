__author__ = 'racktivity'
__tags__ = 'rack', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating rack properties in the model', 3)
    fields = ('name', 'racktype', 'description', 'roomguid', 'floor', 
              'corridor', 'position', 'height', 'tags')
    rack = q.drp.rack.get(params['rackguid'])
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(rack, key, value)
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, fields)
        q.drp.rack.save(rack)
    
    import racktivityui.uigenerator.rack
    racktivityui.uigenerator.rack.update(rack.guid)
        
    params['result'] = {'returncode': True,
                        'rackguid': rack.guid}

def match(q, i, params, tags):
    return True
