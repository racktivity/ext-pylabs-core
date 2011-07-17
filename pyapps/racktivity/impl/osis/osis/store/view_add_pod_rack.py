__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    viewname = 'view_pod_rack'
    records = []
    for rackguid in rootobject.racks:
        records.append({'rack': rackguid})

    osis.viewSave('pod', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'pod'
