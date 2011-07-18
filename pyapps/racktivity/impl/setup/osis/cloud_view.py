__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'cloud'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',q.enumerators.OsisType.STRING,True)
        view.setCol('description',q.enumerators.OsisType.STRING,True)
        view.setCol('smtp',q.enumerators.OsisType.STRING, True)
        view.setCol('smtplogin',q.enumerators.OsisType.STRING, True)
        view.setCol('smtppassword',q.enumerators.OsisType.STRING, True)
        view.setCol('installtype',q.enumerators.OsisType.STRING, True)
        view.setCol('installoption',q.enumerators.OsisType.STRING, True)
        view.setCol('system',q.enumerators.OsisType.BOOLEAN, True)
        view.setCol('cloudusergroupactions',q.enumerators.OsisType.TEXT,True) 
        connection.viewAdd(view)
        indexes = ['name', 'smtppassword',  'smtp', 'smtplogin', 'description']

        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
