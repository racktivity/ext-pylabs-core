__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'user'
    domain = "ui"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name', q.enumerators.OsisType.STRING, True)
        view.setCol('password', q.enumerators.OsisType.STRING, True)
        view.setCol('spaces', q.enumerators.OsisType.STRING, True)
        view.setCol('pages', q.enumerators.OsisType.STRING, True)
        view.setCol('tags', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)

        indexes = ['name', 'tags']
        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
