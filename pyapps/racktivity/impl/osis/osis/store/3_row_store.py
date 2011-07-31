__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    fields = {'name': root.name, 'alias': root.alias, 'roomguid': root.roomguid, 'podguid': root.podguid, 'description': root.description,
              'system': root.system, 'tags': root.tags}
    
    osis.viewSave(params['domain'], 'row', viewname, root.guid, root.version, fields)
    q.logger.log('row saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'row'
