__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'device'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',q.enumerators.OsisType.STRING,True)
        view.setCol('racku',q.enumerators.OsisType.INTEGER,True)
        view.setCol('racky',q.enumerators.OsisType.INTEGER,True)
        view.setCol('rackz',q.enumerators.OsisType.INTEGER,True)
        view.setCol('datacenterguid',q.enumerators.OsisType.UUID,True)
        view.setCol('rackguid',q.enumerators.OsisType.UUID,True)
        view.setCol('cloudspaceguid',q.enumerators.OsisType.UUID,True)
        view.setCol('parentdeviceguid',q.enumerators.OsisType.UUID,True)
        view.setCol('devicetype',q.enumerators.OsisType.STRING,True)
        view.setCol('status',q.enumerators.OsisType.STRING,True)
        view.setCol('template',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('modelnr',q.enumerators.OsisType.STRING,True)
        view.setCol('serialnr',q.enumerators.OsisType.STRING,True)
        view.setCol('firmware',q.enumerators.OsisType.STRING,True)
        view.setCol('description',q.enumerators.OsisType.STRING,True)
        view.setCol('tags', q.enumerators.OsisType.STRING,True)
        connection.viewAdd(view)
        indexes =  ['status', 'rackguid', 'name', 'firmware', 'modelnr', 'cloudspaceguid', 'devicetype', 'template', 'parentdeviceguid', 'serialnr', 'datacenterguid', 'description', 'tags']

        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
