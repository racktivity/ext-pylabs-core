__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_clouduser' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    records = []
    for clouduser in root.cloudusers:
        fields = {'name':root.name, 'clouduserguid':clouduser}
        records.append(fields)

    osis.viewSave(params['domain'], 'cloudusergroup', viewname, root.guid, root.version, records)
    q.logger.log('cloudusergroup_clouduser entry(s) saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'cloudusergroup'
