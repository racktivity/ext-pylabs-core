__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'activity'
    domain = "crm"
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection('main')
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(rootobject, view_name)
        view.setCol('name', q.enumerators.OsisType.STRING, False)
        view.setCol('description', q.enumerators.OsisType.STRING, False)
        view.setCol('customer', q.enumerators.OsisType.STRING, True)
        view.setCol('lead', q.enumerators.OsisType.STRING, True)
        view.setCol('location', q.enumerators.OsisType.STRING, True)
        view.setCol('type', q.enumerators.OsisType.STRING, True)
        view.setCol('priority', q.enumerators.OsisType.STRING, True)
        view.setCol('status', q.enumerators.OsisType.STRING, True)
        view.setCol('starttime', q.enumerators.OsisType.DATETIME, True)
        view.setCol('endtime', q.enumerators.OsisType.DATETIME, True)
        connection.viewAdd(view)
        
        indexes = ['name', 'customer', 'type', 'priority']
        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)