__author__ = 'racktivity'
__tags__ = 'policy', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    if not params['policyguid']:
        q.eventhandler.raiseError('policy guid can not be None or empty string')
    q.logger.log('Deleting policy %s '% params['policyguid'], 3)
    deleted = q.drp.policy.delete(params['policyguid'])
    params['result'] = {'returncode':deleted}

def match(q, i, params, tags):
    return True
