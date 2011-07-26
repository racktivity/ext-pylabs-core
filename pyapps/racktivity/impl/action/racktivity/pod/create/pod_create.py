__author__ = 'racktivity'
__priority__= 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #pod name already exists?
    if exists('racktivity_view_pod_list', p.api.model.racktivity.pod, "name", params['name']):
        raise ValueError("pod with name %s already exists"%params['name'])
    #room exists?
    if not exists('racktivity_view_room_list', p.api.model.racktivity.room, "guid", params['room']):
        raise ValueError("room with guid %s doesn't exists"%params['room'])
    #racks?
    for rackguid in params['racks']:
        if not exists('racktivity_view_rack_list', p.api.model.racktivity.rack, "guid", rackguid):
            raise ValueError("rack with guid %s doesn't exists"%rackguid)
        
    fields = ('name', 'alias', 'description', 'room', 'tags')
    pod = p.api.model.racktivity.pod.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(pod, key, value)
    
    for rackguid in params['racks']:
        pod.racks.append(rackguid)

    p.api.model.racktivity.pod.save(pod)

    params['result'] = {'returncode': True, 'podguid': pod.guid}

    q.logger.log('Creating a policy for pod %s' % pod.name, 3)
    
    p.api.action.racktivity.policy.create('pod_monitor_%s' % pod.name, rootobjecttype='pod', rootobjectaction='monitor',
                                       rootobjectguid=pod.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"])

    podguid = pod.guid
    stores = list()
    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    for type in mtypes:
        stores.append('%s_%s' % (podguid, type))
    
    q.actions.actor.graphdatabase.createStores(stores)

def match(q, i, params, tags):
    return True
