__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'racktivity'
    domain = "racktivity"
    appname = params['appname']
    #use "application" instead of "racktivity_application" because the name becomes too long
    view_name = '%s_view_%s_list' % (domain, "application")
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('sw_version', q.enumerators.OsisType.STRING, True)
        view.setCol('smtp', q.enumerators.OsisType.STRING, True)
        view.setCol('smtplogin', q.enumerators.OsisType.STRING, False)
        view.setCol('smtppassword', q.enumerators.OsisType.STRING, True)
        view.setCol('configured', q.enumerators.OsisType.BOOLEAN, True)
        view.setCol('cloudusergroupactions',q.enumerators.OsisType.TEXT,True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)