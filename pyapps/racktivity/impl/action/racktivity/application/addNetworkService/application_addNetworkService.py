__author__ = 'racktivity'

__priority__ = 3


def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    application = p.api.model.racktivity.application.get(applicationguid)

    ns_name = params['name']
    
    
    existing_service = [ svc for svc in application.networkservices if svc.name == ns_name ]

    if existing_service:
        q.eventhandler.raiseError('Networkservicename %s allready defined for application %s' %(ns_name, applicationguid))
    

    networkservice = application.networkservices.new()
    networkservice.name = ns_name
    networkservice.monitor = params['monitored']
    networkservice.enabled = params['enabled']

    networkservice.ipaddressguids = params['ipaddressguids']
    networkservice.description = params['description']

    application.networkservices.append(networkservice)

    p.api.model.racktivity.application.save(application)

    params['result']= {'returncode':True}

def match(q,i,params,tags):
    return True
