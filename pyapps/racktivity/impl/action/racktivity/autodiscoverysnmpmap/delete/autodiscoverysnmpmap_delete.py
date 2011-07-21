__author__ = 'aserver'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params, nameKey = "manufacturer")
    params['result'] = {'returncode':False}
    guid = params['autodiscoverysnmpmapguid']
    p.api.model.racktivity.autodiscoverysnmpmap.delete(guid)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
