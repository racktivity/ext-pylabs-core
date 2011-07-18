__author__ = 'racktivity'
__tags__ = 'clouduser', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating clouduser properties in the model', 3)
    clouduser = q.drp.clouduser.get(params['clouduserguid'])
    
    paramKeys = ('name','description','email','firstname','lastname','address','city','country',
                 'phonemobile','phonelandline', 'tags')
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(clouduser, paramKey, params[paramKey])
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, paramKeys, nameKey = "login")
        q.drp.clouduser.save(clouduser)
    
    params['result'] = {'returncode': True,
                        'clouduserguid': clouduser.guid}
    
def match(q, i, params, tags):
    return True
