__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags): 
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    application = p.api.model.racktivity.application.get(applicationguid)
    
    if application.status not in (q.enumerators.applicationstatustype.HALTED,
                                  q.enumerators.applicationstatustype.STARTING):
        q.logger.log("Application '%s' in status %s."%(application.name,application.status),1)
        params['result'] = {'returncode':True}
        return
        
    q.logger.log('Starting application "%s"'%application.name)
    try:
        application.status = q.enumerators.applicationstatustype.STARTING
        p.api.model.racktivity.application.save(application)
        p.api.actor.racktivity.application.start(applicationguid)
    except Exception, e:
        q.eventhandler.raiseError('Unable to start application %s. Error: %s'%(application.name, str(e)))
        
    application.status = q.enumerators.applicationstatustype.ACTIVE
    p.api.model.racktivity.application.save(application)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
