__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'lead'
    domain = "crm"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name', q.enumerators.OsisType.STRING, True)
        view.setCol('code', q.enumerators.OsisType.STRING, True)
        view.setCol('customerguid', q.enumerators.OsisType.UUID, True)
        view.setCol('source', q.enumerators.OsisType.STRING, True)
        view.setCol('type', q.enumerators.OsisType.STRING, True)
        view.setCol('status', q.enumerators.OsisType.STRING, True)
        view.setCol('amount', q.enumerators.OsisType.FLOAT, True)
        view.setCol('probability', q.enumerators.OsisType.BIGINT, True)
        connection.viewAdd(view)

        indexes = ['name', 'code', 'source', 'type', 'status', 'amount', 'probability']
        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
