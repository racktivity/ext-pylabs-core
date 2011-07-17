__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'updateModelProperties'
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating cloudusergroup properties in the model', 3)
    cloudusergroup = q.drp.cloudusergroup.get(params['cloudusergroupguid'])

    paramKeys = ('name', 'description', 'tags')
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(cloudusergroup, paramKey, params[paramKey])
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, paramKeys)
        q.drp.cloudusergroup.save(cloudusergroup)
    
    params['result'] = {'returncode': True,
                        'cloudusergroupguid': cloudusergroup.guid}

def match(q, i, params, tags):
    return True
