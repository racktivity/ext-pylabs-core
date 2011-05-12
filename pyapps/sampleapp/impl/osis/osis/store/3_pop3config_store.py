__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection(p.api.appname)
    rootobject = params['rootobject']
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    values = {
        'server': rootobject.server,
        'login': rootobject.login,
        'password': rootobject.password
    }
    osis.viewSave(params['domain'], params['rootobjecttype'], viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'pop3' and params['domain'] == 'config'
