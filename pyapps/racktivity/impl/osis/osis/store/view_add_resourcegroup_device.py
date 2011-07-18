__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    records = []
    for deviceguid in rootobject.deviceguids:
        records.append({'name': rootobject.name, 'device': deviceguid})
    osis.viewSave('resourcegroup', 'view_resourcegroup_device', rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'resourcegroup'