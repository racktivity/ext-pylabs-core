__author__ = 'racktivity'
__tags__ = 'location', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating location properties in the model', 3)
    location = q.drp.location.get(params['locationguid'])
    fields = ('name', 'description', 'alias', 'address', 'city', 'country', 
              'public', 'timezonename', 'timezonedelta', 'tags')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(location, key, value)
            changed = True
    
    if params['coordinatesinfo']:
        coordinates = params['coordinatesinfo']
        location.coordinates.latitude = float(coordinates['latitude'])
        location.coordinates.longitude = float(coordinates['longitude'])
        changed = True
        
    if changed:
        logger.log_tasklet(__tags__, params, fields)
        q.drp.location.save(location)
    
    import racktivityui.uigenerator.campus
    import racktivityui.uigenerator.enterprise
    racktivityui.uigenerator.campus.update(location.guid)
    racktivityui.uigenerator.enterprise.update()

    from rootobjectaction_lib import rootobjectaction_find
    import racktivityui.uigenerator.datacenter
    for dcguid in rootobjectaction_find.datacenter_find(locationguid=location.guid):
        racktivityui.uigenerator.datacenter.update(dcguid)
    
    params['result'] = {'returncode': True,
                        'locationguid': location.guid}

def match(q, i, params, tags):
    return True
