__author__ = 'racktivity'
__tags__ = 'threshold', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    q.logger.log('Deleting threshold %s' % params['thresholdguid'])
    params['result'] = {'returncode': q.drp.threshold.delete(params['thresholdguid'])}

def match(q, i, params, tags):
    return True
