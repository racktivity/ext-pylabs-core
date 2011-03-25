__tags__ = 'osis', 'query'

from osis.store.OsisDB import OsisDB
def main(q, i, p, params, tags):
    con = OsisDB().getConnection(p.api.appname)
    params['result'] = con.runQuery(params['query'])
