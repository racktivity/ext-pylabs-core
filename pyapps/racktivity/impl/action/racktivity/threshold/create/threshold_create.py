__author__ = 'racktivity'
__tags__ = 'threshold', 'create'
__priority__= 3
from logger import logger
from rootobjectaction_lib import events

def main(q, i, params, tags):
    events.raiseCritical("The Threshold is not used anymore")
    
#    logger.log_tasklet(__tags__, params)
#    params['result'] = {'returncode':False}
#    fields = ('thresholdtype',  'minimum', 'maximum',  'thresholdimpacttype', 
#              'clouduserguid', 'tags')
#    threshold = q.drp.threshold.new()
#    for key, value in params.iteritems():
#        if key in fields and value:
#            setattr(threshold, key, value)
#    q.drp.threshold.save(threshold)
#    
#    params['result'] = {'returncode': True,
#                        'thresholdguid': threshold.guid}

def match(q, i, params, tags):
    return True
