__author__ = 'aserver'
__tags__ = 'resourcegroup', 'create'
__priority__= 3
from logger import logger
from rootobjectaction_lib import rootobjectaction_find

def main(q, i, params, tags):
    logger.log_tasklet(__tags__, params)
    resourcegroup = q.drp.resourcegroup.new()
    #params: datacenterguid, name, description, jobguid
    if rootobjectaction_find.resourcegroup_find(params['name']):
        raise ValueError("A resource group with the same name already exists")
    
    resourcegroup.name = params['name']
    resourcegroup.description = params['description']
    acl = resourcegroup.acl.new()
    resourcegroup.acl = acl
    q.drp.resourcegroup.save(resourcegroup)

    from rootobjectaction_lib import rootobject_grant
    rootobject_grant.grantUser(resourcegroup.guid, 'resourcegroup', params['request']['username'])

    params['result'] = {'returncode':True, 'resourcegroupguid': resourcegroup.guid}
    
def match(q, i, params, tags):
    return True
