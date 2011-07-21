__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating backplane properties in the model', 3)
    paramKeys = ('name','description','backplanetype')
    changed = False
    backplane = p.api.model.racktivity.backplane.get(params['backplaneguid'])

    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(backplane, paramKey, params[paramKey])
            changed = True
    if changed:
        #logger.log_tasklet(__tags__, params, paramKeys)
        p.api.model.racktivity.backplane.save(backplane)
    params['result'] = {'returncode':True, 'backplaneguid': backplane.guid}

def match(q, i, params, tags):
    return True
