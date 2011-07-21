__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    if not params['policyguid']:
        q.eventhandler.raiseError('policy guid can not be None or empty string')
    q.logger.log('Deleting policy %s '% params['policyguid'], 3)
    deleted = p.api.model.racktivity.policy.delete(params['policyguid'])
    params['result'] = {'returncode':deleted}

def match(q, i, params, tags):
    return True
