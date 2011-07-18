__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'customer'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',q.enumerators.OsisType.STRING,True)
        view.setCol('description',q.enumerators.OsisType.STRING,True)
        view.setCol('address',q.enumerators.OsisType.STRING,True)
        view.setCol('city',q.enumerators.OsisType.STRING,True)
        view.setCol('country',q.enumerators.OsisType.STRING,True)
        view.setCol('status',q.enumerators.OsisType.STRING,False)
        view.setCol('resourcegroupguid',q.enumerators.OsisType.UUID,True)
        view.setCol('macrange',q.enumerators.OsisType.STRING,True)
        view.setCol('retentionpolicyguid',q.enumerators.OsisType.UUID,True)
        view.setCol('registered',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('tags', q.enumerators.OsisType.STRING,True)
        view.setCol('cloudusergroupactions',q.enumerators.OsisType.TEXT,True)
        connection.viewAdd(view)
        indexes = ['status', 'name', 'resourcegroupguid', 'tags']

        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
