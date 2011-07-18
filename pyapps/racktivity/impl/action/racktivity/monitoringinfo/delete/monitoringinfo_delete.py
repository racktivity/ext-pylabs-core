__author__ = 'racktivity'
__tags__ = 'monitoringinfo', 'delete'
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    params['result'] = q.drp.monitoringinfo.delete(params['monitoringinfoguid'])

def match(q, i, params, tags):
    return True