__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    fields = {'name': root.name,
              'datacenterguid': root.datacenterguid,
              'description': root.description,
              'floor': root.floor,
              'alias': root.alias,
              'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()),
              'tags':root.tags}
    
    osis.viewSave('floor', 'view_floor_list', root.guid, root.version, fields)
    q.logger.log('Floor rootobject saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'floor'
