__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params, nameKey = "sw_version")
    params['result'] = {'returncode': False}
    racktivityguid = params['racktivityguid']
    params['result'] = {'returncode': p.api.model.racktivity.racktivity.delete(racktivityguid)}

def match(q, i, params, tags):
    return True
