__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    fields = {'name': root.name, 'datacenterguid': root.datacenterguid, 'description': root.description, \
              'floorguid': root.floorguid, 'alias': root.alias, 'tags':root.tags}

    osis.viewSave(params['domain'], 'room', viewname, root.guid, root.version, fields)
    q.logger.log('room saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'room'
