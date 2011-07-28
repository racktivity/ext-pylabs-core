__author__ = 'Incubaid'


def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    osis.viewSave(params['domain'], 'clouduser', viewname, root.guid, root.version, {'login': root.login,
                                                                                'name':root.name,
                                                                                'description': root.description,
                                                                                'firstname': root.firstname,
                                                                                'lastname': root.lastname,
                                                                                'address': root.address,
                                                                                'city':root.city,
                                                                                'country':root.country,
                                                                                'status':root.status,
                                                                                'email':root.email,
                                                                                'password':root.password,
                                                                                'system':root.system,
                                                                                'cloudusergroupactions': ','.join(root.cloudusergroupactions.keys()),
                                                                                'tags':root.tags})

    q.logger.log('cloud user saved to view_clouduser_list', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'clouduser'
