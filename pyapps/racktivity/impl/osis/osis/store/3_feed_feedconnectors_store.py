__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_feedconnectors' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    fields = ('status', 'name', 'sequence', 'cableguid')
    records = []
    for feedconnector in rootobject.feedconnectors:
        values = dict()
        for field in fields:
            values[field] = getattr(feedconnector, field)
        records.append(values)
    osis.viewSave(params['domain'], 'feed', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'feed'
