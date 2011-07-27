__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname) 
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    osis.viewDelete(params['domain'], params['rootobjecttype'], viewname, params['rootobjectguid'])

    q.logger.log('Racktivity deleted from view_logicalview_list', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'logicalview'