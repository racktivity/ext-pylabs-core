__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'rack'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',q.enumerators.OsisType.STRING,True)
        view.setCol('datacenterguid',q.enumerators.OsisType.UUID,True)
        view.setCol('roomguid', q.enumerators.OsisType.UUID, True)
        view.setCol('podguid', q.enumerators.OsisType.UUID, True)
        view.setCol('rowguid', q.enumerators.OsisType.UUID, True)
        view.setCol('racktype',q.enumerators.OsisType.STRING,False)
        view.setCol('floor',q.enumerators.OsisType.STRING,True)
        view.setCol('position',q.enumerators.OsisType.STRING,True)
        view.setCol('height',q.enumerators.OsisType.INTEGER,True)
        view.setCol('corridor',q.enumerators.OsisType.STRING,True)
        view.setCol('description',q.enumerators.OsisType.STRING,True)
        view.setCol('tags', q.enumerators.OsisType.STRING,True)
        connection.viewAdd(view)
        indexes = ['name', 'floor', 'height', 'corridor', 'position', 'racktype', 'datacenterguid', 'roomguid', 'description', 'tags']

        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
