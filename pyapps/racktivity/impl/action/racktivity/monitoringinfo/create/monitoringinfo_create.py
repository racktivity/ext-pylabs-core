__author__ = 'racktivity'
__tags__ = 'monitoringinfo', 'create'
from logger import logger

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
     
    fields = ('monitoringdeviceguid', 'portmonitoringlist', 'sensormonitoringlist')
    monitoringinfo = q.drp.monitoringinfo.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(monitoringinfo, key, value)
    q.drp.monitoringinfo.save(monitoringinfo)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(monitoringinfo.guid, 'monitoringinfo', params['request']['username'])

    params['result'] = monitoringinfo.guid

def match(q, i, params, tags):
    return True