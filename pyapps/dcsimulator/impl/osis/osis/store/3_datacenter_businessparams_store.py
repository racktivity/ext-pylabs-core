__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    values = {'name': rootobject.name,
              'collocation': rootobject.collocation,
              'storage': rootobject.storage,
              'cpu': rootobject.cpu,
              'leasebuilding': rootobject.leasebuilding,
              'leaseinfrastructure': rootobject.leaseinfrastructure,
              'leasehw': rootobject.leasehw,
              'interestbuilding': rootobject.interestbuilding,
              'interestdatacenter': rootobject.interestdatacenter,
              'leaseperiodbuilding': rootobject.leaseperiodbuilding,
              'leaseperioddatacenter': rootobject.leaseperioddatacenter,
              'technology': rootobject.technology,
              'installperiod': rootobject.installperiod,
              'size': rootobject.size,
              'racksurface': rootobject.racksurface,
              'kwhourcost': rootobject.kwhourcost,
              'pue': rootobject.pue,
              'salescollocation': rootobject.salescollocation,
              'salescpu': rootobject.salescpu,
              'salesstorage': rootobject.salesstorage,
              'salesbandwidth': rootobject.salesbandwidth
             }
    osis.viewSave(params['domain'], params['rootobjecttype'],viewname, rootobject.guid, rootobject.version, values)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'businessparams' and params['domain'] == 'datacenter'
