__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    
    fields = {'name': root.name, 'clouduserguid': root.clouduserguid,
              'share': root.share, 'cloudusergroupactions': ','.join(root.cloudusergroupactions.keys()), 'tags': root.tags}
    
    osis.viewSave(params['domain'], 'logicalview', viewname, root.guid, root.version, fields)
    q.logger.log('Racktivity logicalview saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'logicalview'
