__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    columns = ('name', 'id', 'template', 'meteringdevicetype', 'parentmeteringdeviceguid', 'rackguid',
               'clouduserguid', 'positionx', 'positiony', 'positionz', 'height',
               'snmpapplicationguid', 'tags', 'meteringdeviceconfigstatus')
    values = dict()
    for col in columns:
        values[col] = getattr(rootobject, col)
    values['cloudusergroupactions'] = ','.join(rootobject.acl.cloudusergroupactions.keys())
    osis.viewSave('meteringdevice', 'view_meteringdevice_list', rootobject.guid, rootobject.version, values)

    q.logger.log('metering device rootobject saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'meteringdevice'
