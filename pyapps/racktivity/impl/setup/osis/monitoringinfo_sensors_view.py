__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'monitoringinfo'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_sensors' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('sensortype', q.enumerators.OsisType.STRING, True)
        view.setCol('value', q.enumerators.OsisType.STRING, True)
        view.setCol('valuemin', q.enumerators.OsisType.STRING, True)
        view.setCol('valuemax', q.enumerators.OsisType.STRING, True)
        view.setCol('value5minuteaverages', q.enumerators.OsisType.STRING, True)
        view.setCol('valueaverage60minutes', q.enumerators.OsisType.STRING, True)
        view.setCol('valuemax60minutes', q.enumerators.OsisType.STRING, True)
        view.setCol('timestamp', q.enumerators.OsisType.DATETIME, True)
        connection.viewAdd(view)