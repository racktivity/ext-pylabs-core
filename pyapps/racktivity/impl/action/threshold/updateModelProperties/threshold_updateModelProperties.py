__author__ = 'racktivity'
__tags__ = 'threshold', 'updateModelProperties'
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    threshold = q.drp.threshold.get(params['thresholdguid'])
    q.logger.log('Updating model properties of threshold %s' % params['thresholdguid'], 3)
    fields = ('thresholdtype', 'minimum', 'maximum', 'thresholdimpacttype', 
              'clouduserguid', 'tags')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(threshold, key, value)
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, fields)
        q.drp.threshold.save(threshold)
    params['result'] = {'returncode': True,
                        'thresholdguid': threshold.guid}

def match(q, i, params, tags):
    return True
