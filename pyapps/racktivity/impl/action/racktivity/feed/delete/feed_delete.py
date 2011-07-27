__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    feedguid = params['feedguid']
    p.api.model.racktivity.feed.delete(feedguid)

    params['result'] = {'returncode':True}
    
def match(q, i, params, tags):
    return True
