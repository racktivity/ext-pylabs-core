__author__ = 'Incubaid'
__tags__ = 'setup'
__priority__= 3

from osis.store.OsisDB import OsisDB

def main(q, i, params, tags):
    rootobject = 'policy'
    domain = "racktivity"
    appname = params['appname']
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection(appname)
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('name',             q.enumerators.OsisType.STRING,  False)
        view.setCol('description',      q.enumerators.OsisType.STRING,  True)
        view.setCol('rootobjecttype',   q.enumerators.OsisType.STRING,  False)
        view.setCol('rootobjectaction', q.enumerators.OsisType.STRING,  False)
        view.setCol('rootobjectguid',   q.enumerators.OsisType.UUID,    True)
        view.setCol('policyparams',     q.enumerators.OsisType.STRING,  True)
        view.setCol('interval',         q.enumerators.OsisType.STRING,  True)
        view.setCol('runbetween',       q.enumerators.OsisType.STRING,  True)
        view.setCol('runnotbetween',    q.enumerators.OsisType.STRING,  True)
        view.setCol('lastrun',          q.enumerators.OsisType.STRING,  True)
        view.setCol('status',           q.enumerators.OsisType.STRING,  True)
        view.setCol('maxruns',          q.enumerators.OsisType.INTEGER, True)
        view.setCol('maxduration',      q.enumerators.OsisType.INTEGER, True)
        view.setCol('tags', q.enumerators.OsisType.STRING,True)
        connection.viewAdd(view)
        indexes = ['rootobjectguid',  'name', 'interval', 'rootobjecttype', 'rootobjectaction', 'description', 'tags']

        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
