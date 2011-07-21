__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    enterpriseguid = params["enterpriseguid"]
    enterprise = p.api.model.racktivity.enterprise.get(enterpriseguid)
    from rootobjectaction_lib import rootobjectaction_list
    
    for location in enterprise.campuses:
        if rootobjectaction_list.location_list(location):
            p.api.action.racktivity.location.delete(location, request = params["request"])
        
    params['result'] = {'returncode': p.api.model.racktivity.enterprise.delete(enterpriseguid)}

def match(q, i, params, tags):
    return True
