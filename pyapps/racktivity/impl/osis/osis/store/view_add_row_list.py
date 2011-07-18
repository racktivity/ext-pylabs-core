__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    
    fields = {'name': root.name, 'alias': root.alias, 'room': root.room, 'pod': root.pod, 'description': root.description,
              'system': root.system, 'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()), 'tags': root.tags}
    
    osis.viewSave('row', 'view_row_list', root.guid, root.version, fields)
    q.logger.log('row saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'row'
