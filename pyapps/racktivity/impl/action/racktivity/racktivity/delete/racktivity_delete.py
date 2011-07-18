__author__ = 'racktivity'
__tags__ = 'racktivity', 'delete'
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params, nameKey = "sw_version")
    params['result'] = {'returncode': False}
    racktivityguid = params['racktivityguid']
    params['result'] = {'returncode': q.drp.racktivity.delete(racktivityguid)}

def match(q, i, params, tags):
    return True
