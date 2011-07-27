__author__ = 'racktivity'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #row name already exists?
    if rootobjectaction_find.find("row", name = params['name']):
        raise ValueError("row with name %s already exists"%params['name'])
    
    if params['roomguid'] == params['podguid']  == None:
        raise ValueError("You need to specify either room or pod guid")
    
    if params['roomguid'] and not rootobjectaction_find.find("room", guid = params['roomguid']):
        raise ValueError("room with guid %s doesn't exists"%params['roomguid'])
    
    if params['podguid'] and not rootobjectaction_find.find("pod", guid = params['podguid']):
        raise ValueError("pod with guid %s doesn't exists"%params['podguid'])

    fields = ('name', 'alias', 'description', 'roomguid', 'podguid', 'tags')
    row = p.api.model.racktivity.row.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(row, key, value)
    
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

    p.api.actor.racktivity.graphdatabase.createStores(stores)

def match(q, i, params, tags):
    return True
