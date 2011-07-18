__author__ = 'racktivity'
__tags__ = 'lan', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    result = q.drp.lan.delete(params['languid'])
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True

