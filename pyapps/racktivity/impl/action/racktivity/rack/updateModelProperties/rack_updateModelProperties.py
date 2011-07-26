__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating rack properties in the model', 3)
    fields = ('name', 'racktype', 'description', 'roomguid', 'floor', 
              'corridor', 'position', 'height', 'tags')
    rack = p.api.model.racktivity.rack.get(params['rackguid'])
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(rack, key, value)
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.rack.save(rack)
    

    params['result'] = {'returncode': True,
                        'rackguid': rack.guid}

def match(q, i, params, tags):
    return True
