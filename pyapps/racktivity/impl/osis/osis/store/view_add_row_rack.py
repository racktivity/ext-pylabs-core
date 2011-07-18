__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    viewname = 'view_row_rack'
    records = []
    for rackguid in rootobject.racks:
        records.append({'rack': rackguid})

    osis.viewSave('row', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'row'
