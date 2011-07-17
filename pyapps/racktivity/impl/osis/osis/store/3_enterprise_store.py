__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    fields = {'name': root.name, 'description': root.description,
              'system': root.system, 'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()), 'tags': root.tags}
    
    osis.viewSave(params['domain'], 'enterprise', viewname, root.guid, root.version, fields)
    q.logger.log('enterprise saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'enterprise'
