__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    fields = {'name':root.name, 'description':root.description, 'cabletype': str(root.cabletype), 'label':root.label, \
              'cloudusergroupactions': ','.join(root.cloudusergroupactions.keys()), 'tags':root.tags}

    osis.viewSave(params['domain'], 'cable', viewname, root.guid, root.version, fields)
    q.logger.log('cable saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'cable'
