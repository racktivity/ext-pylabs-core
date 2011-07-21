__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode': False}
    event = p.api.model.racktivity.meteringdeviceevent.new()
    fields = ('eventtype', 'timestamp', 'level', 'meteringdeviceguid', 'portsequence', 'sensorsequence', 
              'thresholdguid', 'tags', 'errmessagepublic', 'errmessagprivate', 'logs', 'tags')
    map = {'errmessagepublic': 'errormessagepublic', 'errmessageprivate': 'errormessageprivate'}
    for key, value in params.iteritems():
        if key in fields and value not in ['', None]:
            setattr(event, map.get(key, key), value)
    acl = event.acl.new()
    event.acl = acl
    p.api.model.racktivity.meteringdeviceevent.save(event)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(event.guid, 'meteringdeviceevent', params['request']['username'])

    params['result'] = {'returncode': True, 'guid': event.guid}

def match(q, i, params, tags):
    return True