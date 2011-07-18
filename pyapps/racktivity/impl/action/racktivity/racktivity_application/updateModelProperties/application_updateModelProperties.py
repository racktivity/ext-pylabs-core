__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating racktivity_application properties in the model', 3)
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])

    paramKeys = ('name', 'description', 'status', 'customsettings', 'customer', 'monitor', 'template')

    changed = False
    for paramKey in paramKeys:
        if paramKey in params and params[paramKey] <> '':
            setattr(racktivity_application, paramKey, params[paramKey])
            changed = True

    if changed:
        parm = list(params)
        parm["racktivity_applicationguid"] = params["applicationguid"]
        logger.log_tasklet(__tags__, parm, paramKeys)
        q.drp.racktivity_application.save(racktivity_application)
    params['result'] = {'returncode':True, 'applicationguid': racktivity_application.guid}

def match(q, i, params, tags):
    return True
