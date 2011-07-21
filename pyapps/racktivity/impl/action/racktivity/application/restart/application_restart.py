__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])

    if application.status in (q.enumerators.applicationstatustype.ACTIVE,
                              q.enumerators.applicationstatustype.STARTING,
                              q.enumerators.applicationstatustype.STOPPING):
        p.api.action.racktivity.application.stop(params['applicationguid'], request = params["request"])
    
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    
    if application.status == q.enumerators.applicationstatustype.HALTED:
        p.api.action.racktivity.application.start(params['applicationguid'], request = params["request"])
    else:
        q.eventhandler.raiseError("Unable to start '%s' application '%s'." %(application.status,application.name))
    
    params['result'] = {'returncode':True}
    
def match(q, i, params, tags):
    return True
