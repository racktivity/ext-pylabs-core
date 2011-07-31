__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3
import uuid

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'cloudusergroup'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_clouduserrole' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',q.enumerators.OsisType.STRING,True)
        view.setCol('clouduserroleguid',q.enumerators.OsisType.UUID,True)
        view.setCol('role',q.enumerators.OsisType.STRING,True)
        connection.viewAdd(view)
        indexes = ['name','role']

        for field in indexes:
            context = {'index': str(uuid.uuid4()),
                       'schema': "%s_%s" % (domain, rootobject),
                       'view': view_name,
                       'field': field}
            connection.runQuery("""CREATE INDEX "%(index)s" ON %(schema)s.%(view)s (%(field)s)""" % context)
