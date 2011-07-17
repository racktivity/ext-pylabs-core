__author__ = 'racktivity'
__tags__ = 'ipaddress', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating ipaddress properties in the model', 3)
    ipaddress = q.drp.ipaddress.get(params['ipaddressguid'])
    
    paramKeys = ('name','description','address','netmask','block','iptype',
                 'ipversion','languid', 'virtual', 'tags')
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(ipaddress, paramKey, params[paramKey])
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, paramKeys)
        q.drp.ipaddress.save(ipaddress)
    
    params['result'] = {'returncode': True,
                        'ipaddressguid': ipaddress.guid}
    
def match(q, i, params, tags):
    return True
