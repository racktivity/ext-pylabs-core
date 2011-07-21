__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating ipaddress properties in the model', 3)
    ipaddress = p.api.model.racktivity.ipaddress.get(params['ipaddressguid'])
    
    paramKeys = ('name','description','address','netmask','block','iptype',
                 'ipversion','languid', 'virtual', 'tags')
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(ipaddress, paramKey, params[paramKey])
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, paramKeys)
        p.api.model.racktivity.ipaddress.save(ipaddress)
    
    params['result'] = {'returncode': True,
                        'ipaddressguid': ipaddress.guid}
    
def match(q, i, params, tags):
    return True
