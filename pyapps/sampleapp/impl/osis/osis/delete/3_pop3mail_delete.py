__author__ = 'Incubaid'
__priority__= 3

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    osis.viewDelete(params['domain'], params['rootobjecttype'], viewname, params['rootobjectguid'])

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'pop3' and params['domain'] == 'mail'
