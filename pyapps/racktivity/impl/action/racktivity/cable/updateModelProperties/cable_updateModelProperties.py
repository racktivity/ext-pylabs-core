__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating cable properties in the model', 3)
    cable = p.api.model.racktivity.cable.get(params['cableguid'])
    
    paramKeys = ('name','description','cabletype','label', 'tags')
    
    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(cable, paramKey, params[paramKey])
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, paramKeys)
        p.api.model.racktivity.cable.save(cable)
    params['result'] = {'returncode':True, 'cableguid': cable.guid}

def match(q, i, params, tags):
    return True

