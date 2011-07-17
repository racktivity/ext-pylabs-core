__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    
    fields = {'name': root.name, 'alias': root.alias, 'room': root.room, 'description': root.description,
              'system': root.system, 'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()), 'tags': root.tags}
    
    osis.viewSave('pod', 'view_pod_list', root.guid, root.version, fields)
    q.logger.log('pod saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'pod'
