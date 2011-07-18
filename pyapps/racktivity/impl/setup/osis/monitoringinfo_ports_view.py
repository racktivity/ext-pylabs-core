__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'monitoringinfo'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_ports' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('sequence', q.enumerators.OsisType.INTEGER, True)
        view.setCol('status', q.enumerators.OsisType.STRING, True)
        view.setCol('frequency', q.enumerators.OsisType.STRING, True)
        view.setCol('energyactive', q.enumerators.OsisType.STRING, True)
        view.setCol('energyapparent', q.enumerators.OsisType.STRING, True)
        view.setCol('power', q.enumerators.OsisType.STRING, True)
        view.setCol('powermax', q.enumerators.OsisType.STRING, True)
        view.setCol('power5minuteaverages', q.enumerators.OsisType.STRING, True)
        view.setCol('voltagemax', q.enumerators.OsisType.STRING, True)
        view.setCol('voltage', q.enumerators.OsisType.STRING, True)
        view.setCol('voltage5minuteaverages', q.enumerators.OsisType.STRING, True)
        view.setCol('voltageaverage60minutes', q.enumerators.OsisType.STRING, True)
        view.setCol('current', q.enumerators.OsisType.STRING, True)
        view.setCol('currentmax', q.enumerators.OsisType.STRING, True)
        view.setCol('current5minuteaverages', q.enumerators.OsisType.STRING, True)
        view.setCol('currentaverage60minutes', q.enumerators.OsisType.STRING, True)
        view.setCol('powerfactor', q.enumerators.OsisType.STRING, True)
        view.setCol('timestamp', q.enumerators.OsisType.DATETIME, True)
        connection.viewAdd(view)