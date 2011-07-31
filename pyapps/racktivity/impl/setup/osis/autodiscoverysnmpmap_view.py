__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'autodiscoverysnmpmap'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('sysobjectid', q.enumerators.OsisType.STRING, True)
        view.setCol('manufacturer', q.enumerators.OsisType.STRING, True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)
