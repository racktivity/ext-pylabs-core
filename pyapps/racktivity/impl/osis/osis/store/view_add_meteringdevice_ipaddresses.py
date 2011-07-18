__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    viewname = 'view_meteringdevice_ipaddresses'
    records = []
    for nic in rootobject.nics:
        for ipaddressguid in nic.ipaddressguids:
            records.append({'ipaddressguid': ipaddressguid})

    osis.viewSave('meteringdevice', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'meteringdevice'