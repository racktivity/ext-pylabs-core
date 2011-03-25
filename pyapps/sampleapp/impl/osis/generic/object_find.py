__tags__ = 'osis', 'findobject',

from osis.store.OsisDB import OsisDB

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection(p.api.appname)
    params['result'] = osis.objectsFind(params['domain'], 
        params['rootobjecttype'],
        params['filterobject'],
        params['osisview'])
