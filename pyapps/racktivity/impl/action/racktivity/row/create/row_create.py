__author__ = 'racktivity'
__tags__ = 'row', 'create'
__priority__= 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #row name already exists?
    if exists('view_row_list', q.drp.row, "name", params['name']):
        raise ValueError("row with name %s already exists"%params['name'])
    
    if not exists('view_room_list', q.drp.room, "guid", params['room']):
        raise ValueError("room with guid %s doesn't exists"%params['room'])
    
    if not exists('view_pod_list', q.drp.pod, "guid", params['pod']):
        raise ValueError("pod with guid %s doesn't exists"%params['pod'])
    
    #racks?
    for rackguid in params['racks']:
        if not exists('view_rack_list', q.drp.rack, "guid", rackguid):
            raise ValueError("rack with guid %s doesn't exists"%rackguid)

    fields = ('name', 'alias', 'description', 'room', 'pod', 'tags')
    row = q.drp.row.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(row, key, value)
    
    for rackguid in params['racks']:
        row.racks.append(rackguid)
    acl = row.acl.new()
    row.acl = acl
    q.drp.row.save(row)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(row.guid, 'row', params['request']['username'])

    params['result'] = {'returncode': True, 'rowguid': row.guid}
    
    #UI generation
    import racktivityui.uigenerator.row
    racktivityui.uigenerator.row.create(row.guid, row.pod)
    import racktivityui.uigenerator.pod
    racktivityui.uigenerator.pod.update(row.pod)
    
    q.logger.log('Creating a policy for row %s' % row.name, 3)

    q.actions.rootobject.policy.create('row_monitor_%s' % row.name, rootobjecttype='row', rootobjectaction='monitor',
                                       rootobjectguid=row.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"]
                                       )
    
    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name

    rowguid = row.guid
    stores = list()
    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    for type in mtypes:
        stores.append('%s_%s' % (rowguid, type))
    
    q.actions.actor.graphdatabase.createStores(url, stores)

def match(q, i, params, tags):
    return True
