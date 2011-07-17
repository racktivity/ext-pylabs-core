__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    
    fields = {'name': root.name, 'description': root.description,
              'system': root.system, 'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()), 'tags': root.tags}
    
    osis.viewSave('enterprise', 'view_enterprise_list', root.guid, root.version, fields)
    q.logger.log('enterprise saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'enterprise'
