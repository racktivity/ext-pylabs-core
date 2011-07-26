__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    osis.viewSave(params['domain'], 'datacenter', viewname, root.guid, root.version, {'name':root.name,
                                                                                  'locationguid':root.locationguid,
                                                                                  'description':root.description or "",
                                                                                  'clouduserguid':root.clouduserguid,
                                                                                  'latitude': root.coordinates.latitude,
                                                                                  'longitude': root.coordinates.longitude,
                                                                                  'cloudusergroupactions': ','.join(root.cloudusergroupactions.keys()),
                                                                                  'tags':root.tags})

    q.logger.log('Datacenter saved to view_datacenter_list', 3)
    
def match(q, i, params, tags):
    return params['rootobjecttype'] == 'datacenter'
