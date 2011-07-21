__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    logicalviewguid = params["logicalviewguid"]
    params['result'] = {'returncode': p.api.model.racktivity.logicalview.delete(logicalviewguid)}

def match(q, i, params, tags):
    return True


