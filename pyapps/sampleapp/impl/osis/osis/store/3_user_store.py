__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    values = dict()
    values['password'] = rootobject.password
    values['name'] = rootobject.name
    values['groups'] = rootobject.groups
    
    osis.viewSave(params['domain'], params['rootobjecttype'],viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'user' and params['domain'] == 'crm'
