__author__ = 'aserver'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating autodiscoverysnmpmap properties in the model', 3)
    autodiscoverysnmpmap = p.api.model.racktivity.autodiscoverysnmpmap.get(params['autodiscoverysnmpmapguid'])
    
    paramKeys = ('manufacturer', 'sysobjectid', 'tags')
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] is not None:
            setattr(autodiscoverysnmpmap, paramKey, params[paramKey])
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, paramKeys, nameKey = "manufacturer")
        p.api.model.racktivity.autodiscoverysnmpmap.save(autodiscoverysnmpmap)
    params['result'] = {'returncode':True, 'autodiscoverysnmpmapguid': autodiscoverysnmpmap.guid}

def match(q, i, params, tags):
    return True
