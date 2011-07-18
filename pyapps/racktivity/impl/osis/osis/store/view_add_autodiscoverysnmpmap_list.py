__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    osis.viewSave('autodiscoverysnmpmap', 'view_autodiscoverysnmpmap_list',
                  root.guid,
                  root.version,
                  {'manufacturer':root.manufacturer,
                   'sysobjectid':root.sysobjectid,
                   'tags':root.tags})
    q.logger.log('saved', 3)
    
def match(q, i, params, tags):
    return params['rootobjecttype'] == 'autodiscoverysnmpmap'
