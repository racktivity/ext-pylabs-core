__author__ = 'aserver'
__tags__ = 'resourcegroup', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    q.logger.log('Updating resourcegroup properties in the model', 3)
    resourcegroup = q.drp.resourcegroup.get(params['resourcegroupguid'])
    
    paramKeys = ('name', 'description',)
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(resourcegroup, paramKey, params[paramKey])
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, paramKeys)
        q.drp.resourcegroup.save(resourcegroup)
    params['result'] = {'returncode':True, 'resourcegroupguid': resourcegroup.guid}
    
def match(q, i, params, tags):
    return True

