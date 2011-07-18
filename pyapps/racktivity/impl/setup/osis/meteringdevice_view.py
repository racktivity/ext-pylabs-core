__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'meteringdevice'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name', q.enumerators.OsisType.STRING, True)
        view.setCol('id', q.enumerators.OsisType.STRING, True)
        view.setCol('meteringdevicetype', q.enumerators.OsisType.STRING, True)
        view.setCol('meteringdeviceconfigstatus', q.enumerators.OsisType.STRING, True)
        view.setCol('parentmeteringdeviceguid', q.enumerators.OsisType.UUID, True)
        view.setCol('rackguid', q.enumerators.OsisType.UUID, True)
        view.setCol('clouduserguid', q.enumerators.OsisType.UUID, True)
        view.setCol('positionx', q.enumerators.OsisType.INTEGER, True)
        view.setCol('positiony', q.enumerators.OsisType.INTEGER, True)
        view.setCol('positionz', q.enumerators.OsisType.INTEGER, True)
        view.setCol('height', q.enumerators.OsisType.INTEGER, True)
        view.setCol('snmpapplicationguid', q.enumerators.OsisType.UUID, True)
        view.setCol('template', q.enumerators.OsisType.BOOLEAN, True)
        view.setCol('cloudusergroupactions',q.enumerators.OsisType.TEXT,True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)