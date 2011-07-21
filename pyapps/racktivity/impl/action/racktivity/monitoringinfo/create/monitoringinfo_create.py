__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
     
    fields = ('monitoringdeviceguid', 'portmonitoringlist', 'sensormonitoringlist')
    monitoringinfo = p.api.model.racktivity.monitoringinfo.new()
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(monitoringinfo, key, value)
    p.api.model.racktivity.monitoringinfo.save(monitoringinfo)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(monitoringinfo.guid, 'monitoringinfo', params['request']['username'])

    params['result'] = monitoringinfo.guid

def match(q, i, params, tags):
    return True