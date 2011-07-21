__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    cableguid = params['cableguid']
    p.api.model.racktivity.cable.delete(cableguid)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
