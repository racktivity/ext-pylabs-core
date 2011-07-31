__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']

    fields = {'name':root.name, 'description': root.description, 'backplanetype': str(root.backplanetype), 'publicflag':root.publicflag, 'managementflag':root.managementflag, 'storageflag':root.storageflag, 'cloudusergroupactions': ','.join(root.cloudusergroupactions.keys()), 'tags':root.tags}

    osis.viewSave(params['domain'], 'backplane', viewname, root.guid, root.version, fields)
    q.logger.log('backplane saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'backplane'
