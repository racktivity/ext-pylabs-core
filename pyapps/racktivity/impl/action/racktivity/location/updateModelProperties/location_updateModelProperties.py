__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating location properties in the model', 3)
    location = p.api.model.racktivity.location.get(params['locationguid'])
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
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.location.save(location)
    

    params['result'] = {'returncode': True,
                        'locationguid': location.guid}

def match(q, i, params, tags):
    return True
