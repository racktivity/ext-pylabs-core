__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_rack' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    viewname = 'view_pod_rack'
    records = []
    for rackguid in rootobject.racks:
        records.append({'rack': rackguid})

    osis.viewSave(params['domain'], 'pod', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'pod'
