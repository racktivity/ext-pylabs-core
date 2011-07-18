__author__ = 'racktivity'
__tags__ = 'logicalview', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    logicalviewguid = params["logicalviewguid"]
    params['result'] = {'returncode': q.drp.logicalview.delete(logicalviewguid)}

def match(q, i, params, tags):
    return True


