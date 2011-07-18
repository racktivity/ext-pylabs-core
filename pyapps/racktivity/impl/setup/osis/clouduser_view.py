__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'clouduser'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('login',q.enumerators.OsisType.STRING,False)
        view.setCol('name',q.enumerators.OsisType.STRING,True)
        view.setCol('description',q.enumerators.OsisType.STRING,True)
        view.setCol('firstname',q.enumerators.OsisType.STRING,True)
        view.setCol('lastname',q.enumerators.OsisType.STRING,True)
        view.setCol('address',q.enumerators.OsisType.STRING,True)
        view.setCol('city',q.enumerators.OsisType.STRING,True)
        view.setCol('country',q.enumerators.OsisType.STRING,True)
        view.setCol('status',q.enumerators.OsisType.STRING,False)
        view.setCol('email',q.enumerators.OsisType.STRING,True)
        view.setCol('password',q.enumerators.OsisType.STRING,False)
        view.setCol('system',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('tags', q.enumerators.OsisType.STRING,True)
        view.setCol('cloudusergroupactions',q.enumerators.OsisType.TEXT,True)
        connection.viewAdd(view)
        indexes = ['status', 'login', 'email', 'name', 'tags']

        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
