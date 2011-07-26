__author__ = 'racktivity'
__priority__= 3
from logger import logger


def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #Get enterprise guid
    from rootobjectaction_lib import rootobjectaction_find
    enterpriseguid = rootobjectaction_find.enterprise_find()
    if enterpriseguid:
        enterpriseguid = enterpriseguid[0]
    else:
        raise ValueError("You must have an Enterprise before creating new locations")
    #location name already exists?
    if rootobjectaction_find.exists('racktivity_view_location_list', p.api.model.racktivity.location, "name", params['name']):
        raise ValueError("Location with name %s already exists"%params['name'])

    fields = ('name', 'description', 'address', 'alias', 'city', 'country', 'public', 'tags')
    location = p.api.model.racktivity.location.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(location, key, value)
    
    coordinates = location.coordinates.new()
    location.coordinates = coordinates
    
    if params['coordinatesinfo']:
        coordinatesinfo = params['coordinatesinfo']
        coordinates.latitude = float(coordinatesinfo['latitude'])
        coordinates.longitude = float(coordinatesinfo['longitude'])

    p.api.model.racktivity.location.save(location)
    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(location.guid, 'location', params['request']['username'])
    #add the newly created campus/location to the only enterprise in the system
    enterprise = p.api.model.racktivity.enterprise.get(enterpriseguid)
    if location.guid in enterprise.campuses:
        raise ValueError("The campus already exists in enterprise %s"%enterprise.name)
    enterprise.campuses.append(location.guid)
    p.api.model.racktivity.enterprise.save(enterprise)

    #import racktivityui.uigenerator.campus
    #import racktivityui.uigenerator.enterprise
    #racktivityui.uigenerator.campus.create(location.guid)
    #racktivityui.uigenerator.enterprise.update()
    
    q.logger.log('Creating a policy for location %s' % location.name, 3)
    p.api.action.racktivity.policy.create('location_%s' % location.name, rootobjecttype='location', rootobjectaction='monitor',
                                       rootobjectguid=location.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"])

    params['result'] = {'returncode': True,
                        'locationguid': location.guid}

def match(q, i, params, tags):
    return True
