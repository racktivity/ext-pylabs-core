__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    params['result'] = p.api.model.racktivity.monitoringinfo.delete(params['monitoringinfoguid'])

def match(q, i, params, tags):
    return True