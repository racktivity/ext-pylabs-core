__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    
    fields = {'name': root.name, 'clouduserguid': root.clouduserguid,
              'share': root.share, 'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()), 'tags': root.tags}
    
    osis.viewSave('logicalview', 'view_logicalview_list', root.guid, root.version, fields)
    q.logger.log('Racktivity logicalview saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'logicalview'
