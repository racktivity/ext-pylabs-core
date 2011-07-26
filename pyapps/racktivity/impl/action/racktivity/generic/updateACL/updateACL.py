__author__ = 'racktivity'
__tags__ = ('application',
 'backplane',
 'cable',
 'clouduser',
 'cloudusergroup',
 'collector',
 'customer',
 'datacenter',
 'device',
 'enterprise',
 'errorcondition',
 'feed',
 'floor',
 'ipaddress',
 'job',
 'lan',
 'location',
 'logicalview',
 'meteringdevice',
 'meteringdeviceevent',
 'monitoringinfo',
 'pod',
 'policy',
 'rack',
 'racktivity',
 'racktivity_application',
 'resourcegroup',
 'room',
 'row',
 'threshold'), 'updateACL'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(tags, params)
    q.logger.log('params='+str(params))
    params['result'] = {'returncode':False}
    rootobject = getattr(p.api.model.racktivity, tags[0])
    rootobjectinstance = rootobject.get(params['rootobjectguid'])


    rootobjectinstance.cloudusergroupactions = params['cloudusergroupnames']
    rootobject.save(rootobjectinstance)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
