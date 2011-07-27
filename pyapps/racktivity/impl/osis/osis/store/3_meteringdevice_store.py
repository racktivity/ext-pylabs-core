__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_list' % (params['domain'], params['rootobjecttype'])
    rootobject = params['rootobject']
    columns = ('name', 'id', 'template', 'meteringdevicetype', 'parentmeteringdeviceguid', 'rackguid',
               'clouduserguid', 'positionx', 'positiony', 'positionz', 'height', 
               'snmpapplicationguid', 'tags', 'meteringdeviceconfigstatus')
    values = dict()
    for col in columns:
        values[col] = getattr(rootobject, col)
    values["ipaddress"] = rootobject.network.ipaddress if rootobject.network else None
    values['cloudusergroupactions'] = ','.join(rootobject.cloudusergroupactions.keys())
    osis.viewSave(params['domain'], 'meteringdevice', viewname, rootobject.guid, rootobject.version, values)

    q.logger.log('metering device rootobject saved', 3)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'meteringdevice'
