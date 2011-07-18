__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    fields = ('sensortype', 'value', 'valuemin', 'valuemax', 'value5minuteaverages', 'valueaverage60minutes', 'valuemax60minutes', 'timestamp')
    records = []
    for sensor in rootobject.sensors:
        values = dict()
        for field in fields:
            values[field] = getattr(sensor, field)
        records.append(values)
    osis.viewSave('monitoringinfo', 'view_monitoringinfo_sensors', rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'monitoringinfo'
