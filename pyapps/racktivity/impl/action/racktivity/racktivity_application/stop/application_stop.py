__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'stop'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    if racktivity_application.status not in (q.enumerators.applicationstatustype.ACTIVE,
                                  q.enumerators.applicationstatustype.STOPPING,
                                  q.enumerators.applicationstatustype.STARTING):
        q.logger.log("Application '%s' in status %s."%(racktivity_application.name,racktivity_application.status),1)
        params['result'] = {'returncode':False}
        return
    
    try:
        racktivity_application.status = q.enumerators.applicationstatustype.STOPPING
        q.drp.racktivity_application.save(racktivity_application)
        q.actions.actor.racktivity_application.stop(params['applicationguid'])
    except Exception, e:
        q.eventhandler.raiseError('Unable to stop racktivity_application %s. Error: %s'%(racktivity_application.name, str(e)))
    
    racktivity_application.status=q.enumerators.applicationstatustype.HALTED
    q.drp.racktivity_application.save(racktivity_application)
    params['result'] = {'returncode':True}
    
def match(q, i, params, tags):
    return True

