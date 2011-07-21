__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    threshold = p.api.model.racktivity.threshold.get(params['thresholdguid'])
    q.logger.log('Updating model properties of threshold %s' % params['thresholdguid'], 3)
    fields = ('thresholdtype', 'minimum', 'maximum', 'thresholdimpacttype', 
              'clouduserguid', 'tags')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(threshold, key, value)
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.threshold.save(threshold)
    params['result'] = {'returncode': True,
                        'thresholdguid': threshold.guid}

def match(q, i, params, tags):
    return True
