__author__ = 'racktivity'
__tags__ = 'feed', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    feedguid = params['feedguid']
    q.drp.feed.delete(feedguid)
    from racktivityui.uigenerator import deletePage
    deletePage(feedguid)
    
    params['result'] = {'returncode':True}
    
def match(q, i, params, tags):
    return True
