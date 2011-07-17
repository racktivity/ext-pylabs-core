__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'restart'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])

    if racktivity_application.status in (q.enumerators.applicationstatustype.ACTIVE,
                              q.enumerators.applicationstatustype.STARTING,
                              q.enumerators.applicationstatustype.STOPPING):
        q.actions.rootobject.racktivity_application.stop(params['applicationguid'], request = params["request"])
    
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    
    if racktivity_application.status == q.enumerators.applicationstatustype.HALTED:
        q.actions.rootobject.racktivity_application.start(params['applicationguid'], request = params["request"])
    else:
        q.eventhandler.raiseError("Unable to start '%s' racktivity_application '%s'." %(racktivity_application.status,racktivity_application.name))
    
    params['result'] = {'returncode':True}
    
def match(q, i, params, tags):
    return True
