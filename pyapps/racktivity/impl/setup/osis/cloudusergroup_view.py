__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

import uuid
from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'cloudusergroup'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',q.enumerators.OsisType.STRING,True)
        view.setCol('description',q.enumerators.OsisType.STRING,True)
        view.setCol('cloudusergroupactions',q.enumerators.OsisType.TEXT,True)
        connection.viewAdd(view)
        indexes = ['name']

        for field in indexes:
            context = {'index': str(uuid.uuid4()),
                       'schema': "%s_%s" % (domain, rootobject),
                       'view': view_name,
                       'field': field}
            
            connection.runQuery("""CREATE INDEX "%(index)s" ON %(schema)s.%(view)s (%(field)s)""" % context)
