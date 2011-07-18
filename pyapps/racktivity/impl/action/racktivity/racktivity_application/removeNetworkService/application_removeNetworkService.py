__author__='aserver'
__tags__='racktivity_application','removeNetworkService'

__priority__ = 3

def main(q,i,params,tags):
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    racktivity_application = q.drp.racktivity_application.get(applicationguid)

    ns_name = params.get('servicename',None)
    if not ns_name:
        q.eventhandler.raiseError('Please specify the name of the service to be removed !')

    service = [svc for svc in racktivity_application.networkservices if svc.name == ns_name]
    if not service:
        q.eventhandler.raiseError('There is no networkservice named %s in racktivity_application %s' %(ns_name,applicationguid))
    service = service[0]

    racktivity_application.networkservices.remove(service)
    q.drp.racktivity_application.save(racktivity_application)

    params['result'] = {'returncode':True}

def match(q,i,params,tags):
    return True
