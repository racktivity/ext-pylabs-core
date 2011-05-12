__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    values = {
        'name': rootobject.name,
        'code': rootobject.code,
        'customerguid': rootobject.customerguid,
        'source': rootobject.source,
        'type': rootobject.type,
        'status': rootobject.status,
        'amount': rootobject.amount,
        'probability': rootobject.probability
    }
    osis.viewSave(params['domain'], params['rootobjecttype'], viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'lead' and params['domain'] == 'crm'
