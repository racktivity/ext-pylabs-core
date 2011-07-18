__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    osis.viewSave('location', 'view_location_list',
                  root.guid,
                  root.version,
                  {'name':root.name,
                   'alias': root.alias,
                   'address': root.address,
                   'city':root.city,
                   'country':root.country,
                   'description':root.description,
                   'public':root.public,
                   'timezonename':root.timezonename,
                   'timezonedelta':root.timezonedelta,
                   'latitude': root.coordinates.latitude,
                   'longitude': root.coordinates.longitude,
                   'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()),
                   'tags':root.tags})

    q.logger.log('saved', 3)
    
def match(q, i, params, tags):
    return params['rootobjecttype'] == 'location'
