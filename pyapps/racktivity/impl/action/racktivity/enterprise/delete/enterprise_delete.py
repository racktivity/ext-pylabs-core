__author__ = 'racktivity'
__tags__ = 'enterprise', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    enterpriseguid = params["enterpriseguid"]
    enterprise = q.drp.enterprise.get(enterpriseguid)
    from rootobjectaction_lib import rootobjectaction_list
    
    for location in enterprise.campuses:
        if rootobjectaction_list.location_list(location):
            q.actions.rootobject.location.delete(location, request = params["request"])
        
    params['result'] = {'returncode': q.drp.enterprise.delete(enterpriseguid)}

def match(q, i, params, tags):
    return True
