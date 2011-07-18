__author__ = 'racktivity'
__tags__ = ('acl',
 'application',
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

def main(q, i, params, tags):
    logger.log_tasklet(tags, params)
    q.logger.log('params='+str(params))
    params['result'] = {'returncode':False}
    rootobject = getattr(q.drp, tags[0])
    rootobjectinstance = rootobject.get(params['rootobjectguid'])
    acl = rootobjectinstance.acl
    if not acl:
        acl = rootobjectinstance.acl.new()
        rootobjectinstance.acl = acl

    acl.cloudusergroupactions = params['cloudusergroupnames']
    rootobject.save(rootobjectinstance)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
