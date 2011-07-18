__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'lan'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',q.enumerators.OsisType.STRING,True)
        view.setCol('description',q.enumerators.OsisType.STRING,True)
        view.setCol('vlantag',q.enumerators.OsisType.INTEGER,False)
        view.setCol('backplaneguid',q.enumerators.OsisType.UUID,True)
        view.setCol('publicflag',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('managementflag',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('storageflag',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('network',q.enumerators.OsisType.STRING,True)
        view.setCol('netmask',q.enumerators.OsisType.STRING,True)
        view.setCol('gateway',q.enumerators.OsisType.STRING,True)
        view.setCol('startip',q.enumerators.OsisType.STRING,True)
        view.setCol('endip',q.enumerators.OsisType.STRING,True)
        view.setCol('parentlanguid',q.enumerators.OsisType.UUID,True)
        view.setCol('cloudspaceguid',q.enumerators.OsisType.UUID,True)
        view.setCol('status',q.enumerators.OsisType.STRING,False)
        view.setCol('lantype',q.enumerators.OsisType.STRING,False)
        view.setCol('macrange',q.enumerators.OsisType.STRING,True)
        view.setCol('dhcpflag',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('integratedflag', q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('system',q.enumerators.OsisType.BOOLEAN, True)
        view.setCol('tags', q.enumerators.OsisType.STRING,True)
        connection.viewAdd(view)
        indexes = ['status', 'endip', 'publicflag', 'name', 'startip', 'netmask', 'cloudspaceguid', 'parentlanguid', 'network', 'storageflag', 'lantype', 'managementflag', 'dhcpflag', 'gateway', 'vlantag', 'integratedflag','backplaneguid', 'tags']

        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
