__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    values = {
        'server': rootobject.server,
        'login': rootobject.login,
        'password': rootobject.password
    }
    osis.viewSave(params['domain'] , params['rootobjecttype'], viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'eventqueue' and params['domain'] == 'monitoring' 
