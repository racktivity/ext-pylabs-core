__author__ = 'racktivity'
__tags__ = 'datacenter', 'updateModelProperties'
__priority__= 3
from logger import logger

def exists(view, obj, key, value):
    filterObject = obj.getFilterObject()
    filterObject.add(view, key, value, exactMatch=True)
    return len(obj.find(filterObject)) > 0
    

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating datacenter properties in the model', 3)
    keys = ('name','description','locationguid','clouduserguid', 'tags')
    datacenter = q.drp.datacenter.get(params['datacenterguid'])
    #If name is unchanged set it to none
    if datacenter.name == params["name"]:
        params["name"] = None
    #Check if another datacenter with the same name already exist
    if params["name"] and exists('view_datacenter_list', q.drp.datacenter, "name", params['name']):
        raise ValueError("DataCenter with the same name already exists")
    #locationguid is valid?
    if params["locationguid"] and not exists('view_location_list', q.drp.location, "guid", params['locationguid']):
        raise ValueError("Location with guid %s doesn't exist"%params['locationguid'])
    #if clouduserguid is set, make sure its valid
    if params['clouduserguid'] and not exists('view_clouduser_list', q.drp.clouduser, "guid", params['clouduserguid']):
        raise ValueError("clouduser with guid %s doesn't exist"%params['clouduserguid'])

    changed = False

    for key, value in params.iteritems():
        if key in keys and value:
            setattr(datacenter, key, value)
            changed = True
    
    if params['coordinatesinfo']:
        coordinates = params['coordinatesinfo']
        datacenter.coordinates.latitude = float(coordinates['latitude'])
        datacenter.coordinates.longitude = float(coordinates['longitude'])
        changed = True
        
    if changed:
        logger.log_tasklet(__tags__, params, keys)
        q.drp.datacenter.save(datacenter)
    params['result'] = {'returncode': True, 
                        'datacenterguid': datacenter.guid}
    
    import racktivityui.uigenerator.datacenter
    racktivityui.uigenerator.datacenter.update(datacenter.guid)
    import racktivityui.uigenerator.campus
    racktivityui.uigenerator.campus.update(datacenter.locationguid)

def match(q, i, params, tags):
    return True
