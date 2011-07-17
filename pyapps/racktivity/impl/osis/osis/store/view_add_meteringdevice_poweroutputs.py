__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    fields = ('sequence', 'cableguid', 'label')
    records = []
    for poweroutput in rootobject.poweroutputs:
        values = dict()
        for field in fields:
            values[field] = getattr(poweroutput, field)
        records.append(values)
    osis.viewSave('meteringdevice', 'view_meteringdevice_poweroutput', rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'meteringdevice'