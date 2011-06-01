__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'user'
    domain = "crm"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('password', q.enumerators.OsisType.STRING, True)
        view.setCol('name', q.enumerators.OsisType.STRING, True)
        view.setCol('groups', q.enumerators.OsisType.STRING, True)
        connection.viewAdd(view)
        indexes =list()
         
        indexes.append('password')
        indexes.append('name')
        indexes.append('groups')
        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
        
        
        
        
     
