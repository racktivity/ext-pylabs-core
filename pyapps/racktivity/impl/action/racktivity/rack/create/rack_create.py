__author__ = 'racktivity'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    fields = ('name', 'racktype', 'description', 'roomguid', 'floor', 'corridor', 
              'position', 'height', 'tags')
    #Do some checks
    if rootobjectaction_find.find('rack', name = params['name']):
        raise ValueError("Rack with name %s already exists"%params['name'])
    
    roomguid = params['roomguid']
    floorguid = params['floorguid']
    if not roomguid and not floorguid:
        raise ValueError("Can't create a rack with no roomguid or floorguid, at least one is required")
    
    rack = p.api.model.racktivity.rack.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(rack, key, value)

    p.api.model.racktivity.rack.save(rack)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(rack.guid, 'rack', params['request']['username'])

    q.logger.log('Creating a policy for rack %s' % rack.name, 3)
    p.api.action.racktivity.policy.create('rack_%s' % rack.name, rootobjecttype='rack', rootobjectaction='monitor',
                                       rootobjectguid=rack.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"])
    
    params['result'] = {'returncode': True,
                        'rackguid': rack.guid}

def match(q, i, params, tags):
    return True
