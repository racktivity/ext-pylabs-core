__author__ = 'racktivity'
__tags__ = 'pod', 'create'
__priority__= 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #pod name already exists?
    if exists('view_pod_list', q.drp.pod, "name", params['name']):
        raise ValueError("pod with name %s already exists"%params['name'])
    #room exists?
    if not exists('view_room_list', q.drp.room, "guid", params['room']):
        raise ValueError("room with guid %s doesn't exists"%params['room'])
    #racks?
    for rackguid in params['racks']:
        if not exists('view_rack_list', q.drp.rack, "guid", rackguid):
            raise ValueError("rack with guid %s doesn't exists"%rackguid)
        
    fields = ('name', 'alias', 'description', 'room', 'tags')
    pod = q.drp.pod.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(pod, key, value)
    
    for rackguid in params['racks']:
        pod.racks.append(rackguid)
    acl = pod.acl.new()
    pod.acl = acl
    q.drp.pod.save(pod)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(pod.guid, 'pod', params['request']['username'])

    #UI generation
    import racktivityui.uigenerator.pod
    racktivityui.uigenerator.pod.create(pod.guid, pod.room)
    import racktivityui.uigenerator.room
    racktivityui.uigenerator.room.update(pod.room)
    
    params['result'] = {'returncode': True, 'podguid': pod.guid}

    q.logger.log('Creating a policy for pod %s' % pod.name, 3)
    
    q.actions.rootobject.policy.create('pod_monitor_%s' % pod.name, rootobjecttype='pod', rootobjectaction='monitor',
                                       rootobjectguid=pod.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"])
    
    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name

    podguid = pod.guid
    stores = list()
    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    for type in mtypes:
        stores.append('%s_%s' % (podguid, type))
    
    q.actions.actor.graphdatabase.createStores(url, stores)

def match(q, i, params, tags):
    return True
