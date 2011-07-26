__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    osis.viewSave(params['domain'], 'meteringdeviceevent', viewname, root.guid, root.version, {'eventtype': root.eventtype,
                                                                                         'timestamp': root.timestamp,
                                                                                         'level': root.level,
                                                                                         'meteringdeviceguid': root.meteringdeviceguid,
                                                                                         'portsequence': root.portsequence,
                                                                                         'sensorsequence': root.sensorsequence,
                                                                                         'thresholdguid': root.thresholdguid,
                                                                                         'cloudusergroupactions': ','.join(root.cloudusergroupactions.keys()),
                                                                                         'tags': root.tags,
                                                                                         'errormessagepublic':root.errormessagepublic})

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'meteringdeviceevent'