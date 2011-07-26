__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    fields = {'name': root.name,
              'datacenterguid': root.datacenterguid,
              'description': root.description,
              'floor': root.floor,
              'alias': root.alias,
              'cloudusergroupactions': ','.join(root.cloudusergroupactions.keys()),
              'tags':root.tags}
    
    osis.viewSave(params['domain'], 'floor', viewname, root.guid, root.version, fields)
    q.logger.log('Floor rootobject saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'floor'
