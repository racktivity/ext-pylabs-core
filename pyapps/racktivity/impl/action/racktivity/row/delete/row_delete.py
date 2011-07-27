__author__ = 'racktivity'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    rowguid = params["rowguid"]
    row = p.api.model.racktivity.row.get(rowguid)
    
    for rackguid in rootobjectaction_find.find("rack", rowguid=rowguid):
        p.api.action.racktivity.rack.delete(rackguid, request = params["request"])
        
    params['result'] = {'returncode': p.api.model.racktivity.row.delete(rowguid)}

    
    #Delete the policy linked to this roe
    q.logger.log('Deleting policies linked to this row', 3)
    from rootobjectaction_lib import rootobjectaction_find
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=rowguid)
    for policyguid in  policyguids:
        p.api.model.racktivity.policy.delete(policyguid)

    #import racktivityui.uigenerator
    #racktivityui.uigenerator.deletePage(rowguid)
    
    #import racktivityui.uigenerator.pod
    #racktivityui.uigenerator.pod.update(row.pod)
    
def match(q, i, params, tags):
    return True
