__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating application properties in the model', 3)
    application = p.api.model.racktivity.application.get(params['applicationguid'])

    paramKeys = ('name', 'description', 'status', 'customsettings', 'customer', 'monitor', 'template')

    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(application, paramKey, params[paramKey])
            changed = True

    if changed:
        parm = list(params)
        parm["applicationguid"] = params["applicationguid"]
        #logger.log_tasklet(__tags__, parm, paramKeys)
        p.api.model.racktivity.application.save(application)
    params['result'] = {'returncode':True, 'applicationguid': application.guid}

def match(q, i, params, tags):
    return True
