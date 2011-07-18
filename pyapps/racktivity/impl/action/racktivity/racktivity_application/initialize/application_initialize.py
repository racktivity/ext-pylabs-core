__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'initialize'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Calling actor actions to initialize the racktivity_application specified', 3)
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    q.logger.log('Updating racktivity_application status, applicationguid is %s and jobguid is %s' %(racktivity_application.guid, params['jobguid']), 3)
    q.actions.actor.racktivity_application.initialize(jobguid=params['jobguid'], applicationguid=racktivity_application.guid, executionparams = {'description' : 'Initialize the racktivity_application'})
    
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    racktivity_application.status = q.enumerators.applicationstatustype.ACTIVE
    q.drp.racktivity_application.save(racktivity_application)

    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True

