__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'start'
__priority__= 3

def main(q, i, params, tags): 
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    racktivity_application = q.drp.racktivity_application.get(applicationguid)
    
    if racktivity_application.status not in (q.enumerators.applicationstatustype.HALTED,
                                  q.enumerators.applicationstatustype.STARTING):
        q.logger.log("Application '%s' in status %s."%(racktivity_application.name,racktivity_application.status),1)
        params['result'] = {'returncode':True}
        return
        
    q.logger.log('Starting racktivity_application "%s"'%racktivity_application.name)
    try:
        racktivity_application.status = q.enumerators.applicationstatustype.STARTING
        q.drp.racktivity_application.save(racktivity_application)
        q.actions.actor.racktivity_application.start(applicationguid)
    except Exception, e:
        q.eventhandler.raiseError('Unable to start racktivity_application %s. Error: %s'%(racktivity_application.name, str(e)))
        
    racktivity_application.status = q.enumerators.applicationstatustype.ACTIVE
    q.drp.racktivity_application.save(racktivity_application)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
