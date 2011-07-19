__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'application'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_networkports' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('machineguid',q.enumerators.OsisType.UUID,False)
        view.setCol('ipaddress',q.enumerators.OsisType.STRING,True)
        view.setCol('portnr',q.enumerators.OsisType.INTEGER,True)
        view.setCol('portguid',q.enumerators.OsisType.UUID,False)
        view.setCol('ipprotocoltype',q.enumerators.OsisType.STRING,True)
        view.setCol('monitor',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('servicemonitor',q.enumerators.OsisType.BOOLEAN,True)
        connection.viewAdd(view)