__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    values = {'name': rootobject.name, 
              'customer': rootobject.customerguid,
              'lead': rootobject.leadguid,
              'type': rootobject.type, 
              'priority': rootobject.priority,
              'location': rootobject.location,
              'status': rootobject.status,
              'starttime': rootobject.starttime,
              'endtime': rootobject.endtime,
              'description':rootobject.description
              }
    osis.viewSave(params['domain'], params['rootobjecttype'], viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'activity' and params['domain'] == 'crm'
