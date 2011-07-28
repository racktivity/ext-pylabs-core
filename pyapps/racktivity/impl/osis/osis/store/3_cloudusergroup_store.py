__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    osis.viewSave(params['domain'], 'row', viewname, root.guid, root.version, {'name':root.name, 'description': root.description, 'cloudusergroupactions': ','.join(root.cloudusergroupactions.keys())})
    q.logger.log('cloudusergroup saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'cloudusergroup'
