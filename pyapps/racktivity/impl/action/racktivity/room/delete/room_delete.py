__author__ = 'racktivity'
from logger import logger

from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    roomguid = params['roomguid']
    q.logger.log('Deleting room %s' % roomguid, 3)
    
    for podguid in rootobjectaction_find.find("pod", roomguid=roomguid):
        p.api.action.racktivity.pod.delete(podguid, request = params["request"])

    for rowguid in rootobjectaction_find.find("row", roomguid=roomguid):
        p.api.action.racktivity.row.delete(rowguid, request = params["request"])
    
    for rackguid in rootobjectaction_find.find("rack", roomguid=roomguid):
        p.api.action.racktivity.rack.delete(rackguid, request = params["request"])
    
    params['result'] = {'returncode': p.api.model.racktivity.room.delete(roomguid)}

    #import racktivityui.uigenerator.floor
    #import racktivityui.uigenerator

    #racktivityui.uigenerator.deletePage(roomguid)
    #if floorguid:
        #racktivityui.uigenerator.floor.update(floorguid)

    #Delete the policy linked to this room
    q.logger.log('Deleting policies linked to this room', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=roomguid)
    if policyguids:
        policyguid = policyguids[0]
        p.api.model.racktivity.policy.delete(policyguid)

def match(q, i, params, tags):
    return True
