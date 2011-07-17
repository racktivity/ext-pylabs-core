__author__ = 'Incubaid'

def main(q, i, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_services' % (params['domain'], params['rootobjecttype'])
    osis.viewDelete(params['domain'], params['rootobjecttype'], viewname, params['rootobjectguid'])

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'application'
