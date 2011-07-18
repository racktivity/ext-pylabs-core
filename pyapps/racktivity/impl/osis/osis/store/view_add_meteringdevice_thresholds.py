__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    viewname = 'view_meteringdevice_thresholds'
    records = []
    for poweroutput in rootobject.poweroutputs:
        for thresholdguid in poweroutput.thresholdguids:
            records.append({"thresholdguid": thresholdguid})
    for sensor in rootobject.sensors:
        for thresholdguid in sensor.thresholdguids:
            records.append({"thresholdguid": thresholdguid})

    osis.viewSave('meteringdevice', viewname, rootobject.guid, rootobject.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'meteringdevice'