__author__ = 'racktivity'
__tags__ = 'location', 'create'
__priority__= 3
from logger import logger


def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    #Get enterprise guid
    from rootobjectaction_lib import rootobjectaction_find
    enterpriseguid = rootobjectaction_find.enterprise_find()
    if enterpriseguid:
        enterpriseguid = enterpriseguid[0]
    else:
        raise ValueError("You must have an Enterprise before creating new locations")
    #location name already exists?
    if rootobjectaction_find.exists('view_location_list', q.drp.location, "name", params['name']):
        raise ValueError("Location with name %s already exists"%params['name'])

    fields = ('name', 'description', 'address', 'alias', 'city', 'country', 'public', 'tags')
    location = q.drp.location.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(location, key, value)
    
    coordinates = location.coordinates.new()
    location.coordinates = coordinates
    
    if params['coordinatesinfo']:
        coordinatesinfo = params['coordinatesinfo']
        coordinates.latitude = float(coordinatesinfo['latitude'])
        coordinates.longitude = float(coordinatesinfo['longitude'])
    acl = location.acl.new()
    location.acl = acl
    q.drp.location.save(location)
    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(location.guid, 'location', params['request']['username'])
    #add the newly created campus/location to the only enterprise in the system
    enterprise = q.drp.enterprise.get(enterpriseguid)
    if location.guid in enterprise.campuses:
        raise ValueError("The campus already exists in enterprise %s"%enterprise.name)
    enterprise.campuses.append(location.guid)
    q.drp.enterprise.save(enterprise)

    import racktivityui.uigenerator.campus
    import racktivityui.uigenerator.enterprise
    racktivityui.uigenerator.campus.create(location.guid)
    racktivityui.uigenerator.enterprise.update()
    
    q.logger.log('Creating a policy for location %s' % location.name, 3)
    q.actions.rootobject.policy.create('location_%s' % location.name, rootobjecttype='location', rootobjectaction='monitor',
                                       rootobjectguid=location.guid, interval=3.0, runbetween='[("00:00", "24:00")]', runnotbetween='[]',
                                       request = params["request"])

    from rootobjectaction_lib import rootobjectaction_find
    appserverguids = rootobjectaction_find.racktivity_application_find(name='appserverrpc')
    if not appserverguids:
        raise RuntimeError("Application 'appserverrpc' not found/configured")
    
    appserver = q.drp.racktivity_application.get(appserverguids[0])
    url = appserver.networkservices[0].name

    locationguid = location.guid
    stores = list()
    mtypes = ('current', 'voltage', 'frequency', 'activeenergy',
              'apparentenergy', 'powerfactor')
    for type in mtypes:
        stores.append('%s_%s' % (locationguid, type))
    
    q.actions.actor.graphdatabase.createStores(url, stores)


    params['result'] = {'returncode': True,
                        'locationguid': location.guid}

def match(q, i, params, tags):
    return True
