__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_campus' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    records = []
    for campusguid in rootobject.campuses:
        records.append({'campus': campusguid})

    osis.viewSave(params['domain'], 'enterprise', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'enterprise'
