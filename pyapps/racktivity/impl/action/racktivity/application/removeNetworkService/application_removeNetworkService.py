__author__='aserver'

__priority__ = 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    application = p.api.model.racktivity.application.get(applicationguid)

    ns_name = params.get('servicename',None)
    if not ns_name:
        q.eventhandler.raiseError('Please specify the name of the service to be removed !')

    service = [svc for svc in application.networkservices if svc.name == ns_name]
    if not service:
        q.eventhandler.raiseError('There is no networkservice named %s in application %s' %(ns_name,applicationguid))
    service = service[0]

    application.networkservices.remove(service)
    p.api.model.racktivity.application.save(application)

    params['result'] = {'returncode':True}

def match(q,i,params,tags):
    return True
