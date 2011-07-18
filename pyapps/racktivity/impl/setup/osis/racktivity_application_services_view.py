__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'racktivity_application'
    domain = "racktivity"
    appname = params['appname']
    #use "application" instead of "racktivity_application" because the name becomes too long
    view_name = '%s_view_%s_services' % (domain, "application")
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',q.enumerators.OsisType.STRING,False)
        view.setCol('description',q.enumerators.OsisType.STRING,True)
        view.setCol('status',q.enumerators.OsisType.STRING,False)
        view.setCol('template',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('applicationtemplateguid',q.enumerators.OsisType.UUID,True)
        view.setCol('machineguid',q.enumerators.OsisType.UUID,True)
        view.setCol('customsettings',q.enumerators.OsisType.STRING,True)
        view.setCol('servicename',q.enumerators.OsisType.STRING,True)
        view.setCol('servicedescription',q.enumerators.OsisType.STRING,True)
        view.setCol('serviceenabled',q.enumerators.OsisType.BOOLEAN,True)
        view.setCol('service2deviceguid',q.enumerators.OsisType.UUID,True)
        view.setCol('service2applicationguid',q.enumerators.OsisType.UUID,True)
        view.setCol('service2languid',q.enumerators.OsisType.UUID,True)
        view.setCol('service2networkzoneguid',q.enumerators.OsisType.UUID,True)
        view.setCol('service2machineguid',q.enumerators.OsisType.UUID,True)
        view.setCol('service2diskguid',q.enumerators.OsisType.UUID,True)
        view.setCol('service2clouduserguid',q.enumerators.OsisType.UUID,True)
        view.setCol('service2resourcegroupguid',q.enumerators.OsisType.UUID,True)
        view.setCol('meteringdeviceguid',q.enumerators.OsisType.UUID,True)
        connection.viewAdd(view)