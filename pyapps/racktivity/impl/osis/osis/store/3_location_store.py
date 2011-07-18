__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    osis.viewSave(params['domain'], 'location', viewname,
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
