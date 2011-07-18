__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'datacenter'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',q.enumerators.OsisType.STRING,False)
        view.setCol('locationguid',q.enumerators.OsisType.UUID,True)
        view.setCol('clouduserguid',q.enumerators.OsisType.UUID,True)
        view.setCol('description',q.enumerators.OsisType.STRING,True)
        view.setCol('latitude',q.enumerators.OsisType.FLOAT, True)
        view.setCol('longitude',q.enumerators.OsisType.FLOAT, True)
        view.setCol('cloudusergroupactions',q.enumerators.OsisType.TEXT,True)
        view.setCol('tags', q.enumerators.OsisType.STRING,True)
        connection.viewAdd(view)
        indexes = ['clouduserguid', 'locationguid', 'name', 'description', 'tags']

        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
