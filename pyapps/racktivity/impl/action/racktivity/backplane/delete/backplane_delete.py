__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    result = p.api.model.racktivity.backplane.delete(params['backplaneguid'])
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True