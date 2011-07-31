__author__ = 'racktivity'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #pod name already exists?
    if rootobjectaction_find.find("pod", name = params['name']):
        raise ValueError("pod with name %s already exists"%params['name'])
    #room exists?
    if not rootobjectaction_find.find('room', guid = params['roomguid']):
        raise ValueError("room with guid %s doesn't exists"%params['roomguid'])
        
    fields = ('name', 'alias', 'description', 'roomguid', 'tags')
    pod = p.api.model.racktivity.pod.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(pod, key, value)
    
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
    
    p.api.actor.racktivity.graphdatabase.createStores(stores)

def match(q, i, params, tags):
    return True
