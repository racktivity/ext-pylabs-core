__author__ = 'aserver'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    result = p.api.model.racktivity.resourcegroup.delete(params['resourcegroupguid'])
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True

