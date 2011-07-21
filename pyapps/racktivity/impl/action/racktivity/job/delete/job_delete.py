__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    for jobguid in params['jobguids']:
        q.logger.log('Deleting job %s ' % jobguid, 3)
        p.api.model.racktivity.job.delete(jobguid)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
