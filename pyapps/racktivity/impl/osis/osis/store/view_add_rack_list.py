__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    osis.viewSave('rack', 'view_rack_list', root.guid, root.version, {'name':root.name, 'datacenterguid': root.datacenterguid, 'roomguid':root.roomguid,  'racktype': root.racktype, 'floor':root.floor, 'position':root.position, 'height':root.height, 'corridor':root.corridor, 'description':root.description, 'tags':root.tags})

    q.logger.log('saved', 3)
    
def match(q, i, params, tags):
    return params['rootobjecttype'] == 'rack'
