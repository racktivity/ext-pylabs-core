__author__ = 'Incubaid'


from osis.store.OsisDB import OsisDB

def main(q, i, p, params, tags):
    rootobject = 'businessparams'
    domain = "datacenter"
    view_name = '%s_view_%s_list' % (domain, rootobject)
    connection = OsisDB().getConnection('dcsimulator')
    if not connection.viewExists(domain, rootobject, view_name):
        view = connection.viewCreate(domain, rootobject, view_name)
        view.setCol('collocation', q.enumerators.OsisType.INTEGER, True)
        view.setCol('storage', q.enumerators.OsisType.INTEGER, True)
        view.setCol('cpu', q.enumerators.OsisType.INTEGER, True)
        view.setCol('leasebuilding', q.enumerators.OsisType.INTEGER, True)
        view.setCol('leaseinfrastructure', q.enumerators.OsisType.INTEGER, True)
        view.setCol('leasehw', q.enumerators.OsisType.INTEGER, True)
        view.setCol('interestbuilding', q.enumerators.OsisType.FLOAT, True)
        view.setCol('interestdatacenter', q.enumerators.OsisType.FLOAT, True)
        view.setCol('leaseperiodbuilding', q.enumerators.OsisType.INTEGER, True)
        view.setCol('leaseperioddatacenter', q.enumerators.OsisType.INTEGER, True)
        view.setCol('technology', q.enumerators.OsisType.INTEGER, True)
        view.setCol('installperiod', q.enumerators.OsisType.INTEGER, True)
        view.setCol('size', q.enumerators.OsisType.INTEGER, False)
        view.setCol('racksurface', q.enumerators.OsisType.INTEGER, False)
        view.setCol('kwhourcost', q.enumerators.OsisType.FLOAT, False)
        view.setCol('pue', q.enumerators.OsisType.FLOAT, False)
        view.setCol('salescollocation', q.enumerators.OsisType.FLOAT, False)
        view.setCol('salescpu', q.enumerators.OsisType.FLOAT, False)
        view.setCol('salesstorage', q.enumerators.OsisType.FLOAT, False)
        view.setCol('salesbandwidth', q.enumerators.OsisType.FLOAT, False)
        connection.viewAdd(view)
        
        indexes = ['collocation', 'size', 'leasebuilding', 'interestdatacenter']
        for field in indexes:
            context = {'schema': "%s_%s" % (domain, rootobject), 'view': view_name, 'field': field}
            connection.runQuery("CREATE INDEX %(field)s_%(schema)s_%(view)s ON %(schema)s.%(view)s (%(field)s)" % context)
