__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating clouduser properties in the model', 3)
    clouduser = p.api.model.racktivity.clouduser.get(params['clouduserguid'])
    
    paramKeys = ('name','description','email','firstname','lastname','address','city','country',
                 'phonemobile','phonelandline', 'tags')
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(clouduser, paramKey, params[paramKey])
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, paramKeys, nameKey = "login")
        p.api.model.racktivity.clouduser.save(clouduser)
    
    params['result'] = {'returncode': True,
                        'clouduserguid': clouduser.guid}
    
def match(q, i, params, tags):
    return True
