__author__ = 'racktivity'
__tags__ = 'backplane', 'updateModelProperties'
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating backplane properties in the model', 3)
    paramKeys = ('name','description','backplanetype')
    changed = False
    backplane = q.drp.backplane.get(params['backplaneguid'])

    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(backplane, paramKey, params[paramKey])
            changed = True
    if changed:
        logger.log_tasklet(__tags__, params, paramKeys)
        q.drp.backplane.save(backplane)
    params['result'] = {'returncode':True, 'backplaneguid': backplane.guid}

def match(q, i, params, tags):
    return True
