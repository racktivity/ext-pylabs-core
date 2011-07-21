__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    ipaddress = p.api.model.racktivity.ipaddress.get(params['ipaddressguid'])
    languid = ipaddress.languid
     
    params['result'] = {'returncode': p.api.model.racktivity.ipaddress.delete(ipaddress.guid)}
            

def match(q, i, params, tags):
    return True

