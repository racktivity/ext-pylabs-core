__author__ = 'racktivity'
__tags__ = 'backplane', 'delete'
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    result = q.drp.backplane.delete(params['backplaneguid'])
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True