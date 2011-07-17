__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    viewname = 'view_enterprise_campus'
    records = []
    for campusguid in rootobject.campuses:
        records.append({'campus': campusguid})

    osis.viewSave('enterprise', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'enterprise'
