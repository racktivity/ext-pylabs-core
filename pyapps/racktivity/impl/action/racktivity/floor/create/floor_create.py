__author__ = 'racktivity'
__priority__ = 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    q.logger.log('Creating new floor', 4)
    fields = ('name', 'description', 'datacenterguid', 'floor', 'alias', 'tags')
    #Do some checks
    if exists('racktivity_view_floor_list', p.api.model.racktivity.floor, "name", params['name']):
        raise ValueError("Floor with name %s already exists"%params['name'])
    if not exists('racktivity_view_datacenter_list', p.api.model.racktivity.datacenter, "guid", params['datacenterguid']):
        raise ValueError("Invalid datacenterguid %s"%params['datacenterguid'])
    
    floor = p.api.model.racktivity.floor.new()
    for key, value in params.iteritems():
        if key in fields and value not in (None, ""):
            setattr(floor, key, value)

    p.api.model.racktivity.floor.save(floor)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(floor.guid, 'floor', params['request']['username'])

    q.logger.log('Creating a policy for floor %s' % floor.name, 3)
    p.api.action.racktivity.policy.create('floor_%s' % floor.name, rootobjecttype='floor', rootobjectaction='monitor',
                                       rootobjectguid=floor.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]', request = params["request"])

    #Generate UI page
    #import racktivityui.uigenerator.datacenter
    #import racktivityui.uigenerator.floor

    #racktivityui.uigenerator.floor.create(floor.guid, floor.datacenterguid)
    #racktivityui.uigenerator.datacenter.update(floor.datacenterguid)

    params['result'] = {'returncode': True,
                        'floorguid': floor.guid}

def match(q, i, params, tags):
    return True
