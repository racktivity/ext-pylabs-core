__author__ = 'racktivity'
__tags__ = 'lan', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating lan properties in the model', 3)
    lan = q.drp.lan.get(params['languid'])
    
    paramKeys = ('name','description','gateway', 'network', 'netmask', 
                 'startip', 'endip', 'tags')
    
    changed = []
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(lan, paramKey, params[paramKey])
            changed.append(paramKey)
    if changed:
        logger.log_tasklet(__tags__, params, paramKeys)
        q.drp.lan.save(lan)

    params['result'] = {'returncode': True,
                        'languid': lan.guid}

def match(q, i, params, tags):
    return True
