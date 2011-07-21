__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating logicalview properties in the model', 3)
    logicalview = p.api.model.racktivity.logicalview.get(params['logicalviewguid'])
    fields = ('name', 'description', 'viewstring', 'clouduserguid', 'share', 'tags')
    
    changed = False

    for key, value in params.iteritems():
        if key in fields and value != '':
            setattr(logicalview, key, value)
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.logicalview.save(logicalview)
    
    params['result'] = {'returncode': True,
                        'logicalviewguid': logicalview.guid}
def match(q, i, params, tags):
    return True
