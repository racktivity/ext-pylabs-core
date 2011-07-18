__author__ = 'racktivity'
__tags__ = 'rack', 'delete'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    rackguid = params['rackguid']
    rack = q.drp.rack.get(rackguid)
    q.logger.log('Deleting rack %s' % rackguid)
    from rootobjectaction_lib import rootobjectaction_find, rootobjectaction_list
    devices = rootobjectaction_find.device_find(rackguid=rackguid)
    meteringdevices = rootobjectaction_list.meteringdevice_list(rackguid=rackguid)
    for deviceguid in devices:
        q.actions.rootobject.device.delete(deviceguid, request = params["request"])
    for meteringdevice in meteringdevices:
        if not meteringdevice["parentmeteringdeviceguid"]:
            q.actions.rootobject.meteringdevice.delete(meteringdevice["guid"], request = params["request"])
    params['result'] = {'returncode': q.drp.rack.delete(params['rackguid'])}
    
    parentFound = False
    #remove from any potential row.
    for rowguid in rootobjectaction_find.row_find(rack=rackguid):
        parentFound = True
        q.actions.rootobject.row.removeRack(rowguid, rackguid, request = params["request"])
    
    if not parentFound:
        #remove from any potential pod
        for podguid in rootobjectaction_find.pod_find(rack=rackguid):
            parentFound = True
            q.actions.rootobject.pod.removeRack(podguid, rackguid, request = params["request"])
    
    if not parentFound and rack.roomguid:
        #update room page.
        parentFound = True
        import racktivityui.uigenerator.room
        racktivityui.uigenerator.room.update(rack.roomguid)
    
    if not parentFound and rack.floor:
        parentFound = True
        import racktivityui.uigenerator.floor
        racktivityui.uigenerator.floor.update(rack.floor)
        
    import racktivityui.uigenerator
    racktivityui.uigenerator.deletePage(rackguid)

    #Delete the policy linked to this rack
    q.logger.log('Deleting policies linked to this rack', 3)
    policyguids = rootobjectaction_find.policy_find(rootobjectguid=rackguid)
    if policyguids:
        policyguid = policyguids[0]
        q.drp.policy.delete(policyguid)

    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name
    
    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    databasenames = []
    for type in mtypes:
        databasenames.append('%s_%s' % (rackguid, type))

    q.actions.actor.graphdatabase.destroyStores(url, databasenames)

def match(q, i, params, tags):
    return True
