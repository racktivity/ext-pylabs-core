__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    values = dict()
    values['name'] = rootobject.name
    values['permissions'] = rootobject.permissions
    
    osis.viewSave(params['domain'], params['rootobjecttype'],viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'group' and params['domain'] == 'crm'
