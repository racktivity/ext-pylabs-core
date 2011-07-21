__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_poweroutput' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    fields = ('sequence', 'cableguid', 'label')
    records = []
    for poweroutput in rootobject.poweroutputs:
        values = dict()
        for field in fields:
            values[field] = getattr(poweroutput, field)
        records.append(values)
    osis.viewSave(params['domain'], 'meteringdevice', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'meteringdevice'
