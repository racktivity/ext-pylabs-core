__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'pod'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_rack' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('rack', q.enumerators.OsisType.UUID, True)
        connection.viewAdd(view)