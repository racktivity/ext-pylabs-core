__author__ = 'racktivity'
__tags__ = 'errorcondition', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    params['result'] = {'returncode': q.drp.errorcondition.delete(params['errorconditionguid'])}

def match(q, i, params, tags):
    return True
