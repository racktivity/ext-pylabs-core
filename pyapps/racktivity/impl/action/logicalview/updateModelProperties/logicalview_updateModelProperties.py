__author__ = 'racktivity'
__tags__ = 'logicalview', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating logicalview properties in the model', 3)
    logicalview = q.drp.logicalview.get(params['logicalviewguid'])
    fields = ('name', 'description', 'viewstring', 'clouduserguid', 'share', 'tags')
    
    changed = False

    for key, value in params.iteritems():
        if key in fields and value != '':
            setattr(logicalview, key, value)
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, fields)
        q.drp.logicalview.save(logicalview)
    
    params['result'] = {'returncode': True,
                        'logicalviewguid': logicalview.guid}
def match(q, i, params, tags):
    return True
