__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    fields = ('status', 'name', 'sequence', 'cableguid')
    records = []
    for feedconnector in rootobject.feedconnectors:
        values = dict()
        for field in fields:
            values[field] = getattr(feedconnector, field)
        records.append(values)
    osis.viewSave('feed', 'view_feed_feedconnectors', rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'feed'
