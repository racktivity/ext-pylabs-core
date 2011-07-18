__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'feed'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('datacenterguid', q.enumerators.OsisType.UUID, True)
        view.setCol('name', q.enumerators.OsisType.STRING, False)
        view.setCol('description', q.enumerators.OsisType.STRING, True)
        view.setCol('productiontype', q.enumerators.OsisType.STRING, False)
        view.setCol('system', q.enumerators.OsisType.BOOLEAN, True)
        view.setCol('cloudusergroupactions',q.enumerators.OsisType.TEXT,True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)