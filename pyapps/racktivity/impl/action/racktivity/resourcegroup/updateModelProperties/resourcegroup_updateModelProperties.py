__author__ = 'aserver'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    q.logger.log('Updating resourcegroup properties in the model', 3)
    resourcegroup = p.api.model.racktivity.resourcegroup.get(params['resourcegroupguid'])
    
    paramKeys = ('name', 'description',)
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(resourcegroup, paramKey, params[paramKey])
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, paramKeys)
        p.api.model.racktivity.resourcegroup.save(resourcegroup)
    params['result'] = {'returncode':True, 'resourcegroupguid': resourcegroup.guid}
    
def match(q, i, params, tags):
    return True

