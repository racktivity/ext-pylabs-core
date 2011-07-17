__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    osis.viewSave(params['domain'], 'rack', viewname, root.guid, root.version, {'name':root.name, 'datacenterguid': root.datacenterguid, 'roomguid':root.roomguid,  'racktype': root.racktype, 'floor':root.floor, 'position':root.position, 'height':root.height, 'corridor':root.corridor, 'description':root.description, 'tags':root.tags})

    q.logger.log('saved', 3)
    
def match(q, i, params, tags):
    return params['rootobjecttype'] == 'rack'
