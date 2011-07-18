__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_ports' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    fields = ('sequence', 'status', 'frequency', 'energyactive', 'energyapparent', 'power', 'powermax', 'power5minuteaverages', 'voltage', 
              'voltagemax', 'voltage5minuteaverages', 'voltageaverage60minutes', 'current', 'currentmax', 'current5minuteaverages', 'currentaverage60minutes', 
              'powerfactor', 'timestamp')
    records = []
    for port in rootobject.ports:
        values = dict()
        for field in fields:
            values[field] = getattr(port, field)
        records.append(values)
    osis.viewSave(params['domain'], 'monitoringinfo', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'monitoringinfo'
