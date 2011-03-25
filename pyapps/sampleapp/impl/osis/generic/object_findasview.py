__tags__ = 'osis', 'findasview',

from osis.store.OsisDB import OsisDB

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection(p.api.appname)
    params['result'] = osis.objectsFindAsView(params['domain'],
        params['rootobjecttype'],
        params['filterobject'],
        params['osisview'])
