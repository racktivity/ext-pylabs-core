__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    root = params['rootobject']
    osis.viewSave('meteringdeviceevent','view_meteringdeviceevent_list', root.guid, root.version, {'eventtype': root.eventtype,
                                                                                         'timestamp': root.timestamp,
                                                                                         'level': root.level,
                                                                                         'meteringdeviceguid': root.meteringdeviceguid,
                                                                                         'portsequence': root.portsequence,
                                                                                         'sensorsequence': root.sensorsequence,
                                                                                         'thresholdguid': root.thresholdguid,
                                                                                         'cloudusergroupactions': ','.join(root.acl.cloudusergroupactions.keys()),
                                                                                         'tags': root.tags,
                                                                                         'errormessagepublic':root.errormessagepublic})

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'meteringdeviceevent'