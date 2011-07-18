__author__ = 'racktivity'
__tags__ = 'cable', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    cableguid = params['cableguid']
    q.drp.cable.delete(cableguid)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
