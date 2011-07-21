__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    q.logger.log('Deleting threshold %s' % params['thresholdguid'])
    params['result'] = {'returncode': p.api.model.racktivity.threshold.delete(params['thresholdguid'])}

def match(q, i, params, tags):
    return True
