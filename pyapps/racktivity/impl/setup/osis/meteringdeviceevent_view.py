__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'meteringdeviceevent'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('eventtype', q.enumerators.OsisType.STRING, True)
        view.setCol('timestamp', q.enumerators.OsisType.INTEGER,True)
        view.setCol('level', q.enumerators.OsisType.INTEGER, True)
        view.setCol('meteringdeviceguid', q.enumerators.OsisType.UUID, True)
        view.setCol('portsequence', q.enumerators.OsisType.INTEGER, True)
        view.setCol('sensorsequence', q.enumerators.OsisType.INTEGER, True)
        view.setCol('thresholdguid', q.enumerators.OsisType.UUID, True)
        view.setCol('cloudusergroupactions',q.enumerators.OsisType.TEXT,True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True)
        view.setCol('errormessagepublic', q.enumerators.OsisType.TEXT, True)
        connection.viewAdd(view)