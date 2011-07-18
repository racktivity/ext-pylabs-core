__author__ = 'racktivity'
__tags__ = 'job', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    for jobguid in params['jobguids']:
        q.logger.log('Deleting job %s ' % jobguid, 3)
        q.drp.job.delete(jobguid)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
