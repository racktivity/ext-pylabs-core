__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    osis.viewSave(params['domain'], 'autodiscoverysnmpmap', viewname,
                  root.guid,
                  root.version,
                  {'manufacturer':root.manufacturer,
                   'sysobjectid':root.sysobjectid,
                   'tags':root.tags})
    q.logger.log('saved', 3)
    
def match(q, i, params, tags):
    return params['rootobjecttype'] == 'autodiscoverysnmpmap'
