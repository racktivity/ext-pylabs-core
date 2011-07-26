__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    rackguid = params['rackguid']
    rack = p.api.model.racktivity.rack.get(rackguid)
    q.logger.log('Deleting rack %s' % rackguid)
    from rootobjectaction_lib import rootobjectaction_find, rootobjectaction_list
    devices = rootobjectaction_find.device_find(rackguid=rackguid)
    meteringdevices = rootobjectaction_list.meteringdevice_list(rackguid=rackguid)
    for deviceguid in devices:
        p.api.action.racktivity.device.delete(deviceguid, request = params["request"])
    for meteringdevice in meteringdevices:
        if not meteringdevice["parentmeteringdeviceguid"]:
            p.api.action.racktivity.meteringdevice.delete(meteringdevice["guid"], request = params["request"])
    params['result'] = {'returncode': p.api.model.racktivity.rack.delete(params['rackguid'])}
    
    parentFound = False
    #remove from any potential row.
    for rowguid in rootobjectaction_find.row_find(rack=rackguid):
        parentFound = True
        p.api.action.racktivity.row.removeRack(rowguid, rackguid, request = params["request"])
    
    if not parentFound:
        #remove from any potential pod
        for podguid in rootobjectaction_find.pod_find(rack=rackguid):
            parentFound = True
            p.api.action.racktivity.pod.removeRack(podguid, rackguid, request = params["request"])


    #Delete the policy linked to this rack
    q.logger.log('Deleting policies linked to this rack', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=rackguid)
    if policyguids:
        policyguid = policyguids[0]
        p.api.model.racktivity.policy.delete(policyguid)

    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (rackguid, type))

    p.api.actor.graphdatabase.destroyStores(databasenames)

def match(q, i, params, tags):
    return True
