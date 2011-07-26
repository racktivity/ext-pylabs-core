__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Calling actor actions to initialize the application specified', 3)
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    q.logger.log('Updating application status, applicationguid is %s and jobguid is %s' %(application.guid, params['jobguid']), 3)
    p.api.actor.application.initialize(jobguid=params['jobguid'], applicationguid=application.guid, executionparams = {'description' : 'Initialize the application'})
    
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    application.status = q.enumerators.applicationstatustype.ACTIVE
    p.api.model.racktivity.application.save(application)

    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True

