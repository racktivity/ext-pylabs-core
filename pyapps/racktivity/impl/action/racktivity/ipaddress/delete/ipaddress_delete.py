__author__ = 'racktivity'
__tags__ = 'ipaddress', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    ipaddress = q.drp.ipaddress.get(params['ipaddressguid'])
    languid = ipaddress.languid
     
    params['result'] = {'returncode': q.drp.ipaddress.delete(ipaddress.guid)}
            

def match(q, i, params, tags):
    return True

