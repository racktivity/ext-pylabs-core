__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_clouduserrole' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    records = []
    for clouduserrole in root.clouduserroles:
        fields = {'name': root.name, 
                  'clouduserroleguid': clouduserrole}
        records.append(fields)

    osis.viewSave(params['domain'], 'row', viewname, root.guid, root.version, records)
    q.logger.log('cloudusergroup_clouduserrole entry(s) saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'cloudusergroup'
