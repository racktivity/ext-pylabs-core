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
    #row name already exists?
    if exists('racktivity_view_row_list', p.api.model.racktivity.row, "name", params['name']):
        raise ValueError("row with name %s already exists"%params['name'])
    
    if not exists('racktivity_view_room_list', p.api.model.racktivity.room, "guid", params['room']):
        raise ValueError("room with guid %s doesn't exists"%params['room'])
    
    if not exists('racktivity_view_pod_list', p.api.model.racktivity.pod, "guid", params['pod']):
        raise ValueError("pod with guid %s doesn't exists"%params['pod'])
    
    #racks?
    for rackguid in params['racks']:
        if not exists('racktivity_view_rack_list', p.api.model.racktivity.rack, "guid", rackguid):
            raise ValueError("rack with guid %s doesn't exists"%rackguid)

    fields = ('name', 'alias', 'description', 'room', 'pod', 'tags')
    row = p.api.model.racktivity.row.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(row, key, value)
    
    for rackguid in params['racks']:
        row.racks.append(rackguid)

    p.api.model.racktivity.row.save(row)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(row.guid, 'row', params['request']['username'])

    params['result'] = {'returncode': True, 'rowguid': row.guid}


    q.logger.log('Creating a policy for row %s' % row.name, 3)

    p.api.action.racktivity.policy.create('row_monitor_%s' % row.name, rootobjecttype='row', rootobjectaction='monitor',
                                       rootobjectguid=row.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"]
                                       )

    rowguid = row.guid
    stores = list()
    mtypes = ('current', 'voltage', 'frequency',  'activeenergy',
              'apparentenergy', 'powerfactor')
    for type in mtypes:
        stores.append('%s_%s' % (rowguid, type))

    q.actions.actor.graphdatabase.createStores(stores)

def match(q, i, params, tags):
    return True
