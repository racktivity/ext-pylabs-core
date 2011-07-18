__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_campus' % (params['domain'], params['rootobjecttype'])
    osis.viewDelete(params['domain'], params['rootobjecttype'], viewname, params['rootobjectguid'])

    q.logger.log('campus deleted from view_enterprise_campus', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'enterprise'
