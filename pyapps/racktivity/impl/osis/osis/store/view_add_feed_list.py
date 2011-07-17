__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    fields = {'datacenterguid': root.datacenterguid, 'name': root.name, 'description': root.description, \
              'productiontype': root.productiontype, 'system': root.system, 'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()), \
              'tags': root.tags}
    osis.viewSave('feed', 'view_feed_list', root.guid, root.version, fields)
    q.logger.log('feed rootobject saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'feed'
