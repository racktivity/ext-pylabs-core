__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    if application.status not in (q.enumerators.applicationstatustype.ACTIVE,
                                  q.enumerators.applicationstatustype.STOPPING,
                                  q.enumerators.applicationstatustype.STARTING):
        q.logger.log("Application '%s' in status %s."%(application.name,application.status),1)
        params['result'] = {'returncode':False}
        return
    
    try:
        application.status = q.enumerators.applicationstatustype.STOPPING
        p.api.model.racktivity.application.save(application)
        p.api.actor.racktivity.application.stop(params['applicationguid'])
    except Exception, e:
        q.eventhandler.raiseError('Unable to stop application %s. Error: %s'%(application.name, str(e)))
    
    application.status=q.enumerators.applicationstatustype.HALTED
    p.api.model.racktivity.application.save(application)
    params['result'] = {'returncode':True}
    
def match(q, i, params, tags):
    return True

