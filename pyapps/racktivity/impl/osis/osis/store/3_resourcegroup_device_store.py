__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_device' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    records = []
    for deviceguid in rootobject.deviceguids:
        records.append({'name': rootobject.name, 'device': deviceguid})
    osis.viewSave(params['domain'], 'resourcegroup', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'resourcegroup'