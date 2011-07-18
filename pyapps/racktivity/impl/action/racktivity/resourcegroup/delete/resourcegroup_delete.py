__author__ = 'aserver'
__tags__ = 'resourcegroup', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    result = q.drp.resourcegroup.delete(params['resourcegroupguid'])
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True

