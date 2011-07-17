__author__ = 'racktivity'
__tags__= 'racktivity_application','addNetworkService'

__priority__ = 3


def main(q,i,params,tags):
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    racktivity_application = q.drp.racktivity_application.get(applicationguid)

    ns_name = params['name']
    
    
    existing_service = [ svc for svc in racktivity_application.networkservices if svc.name == ns_name ]

    if existing_service:
        q.eventhandler.raiseError('Networkservicename %s allready defined for racktivity_application %s' %(ns_name, applicationguid))
    

    networkservice = racktivity_application.networkservices.new()
    networkservice.name = ns_name
    networkservice.monitor = params['monitored']
    networkservice.enabled = params['enabled']

    networkservice.ipaddressguids = params['ipaddressguids']
    networkservice.description = params['description']

    racktivity_application.networkservices.append(networkservice)

    q.drp.racktivity_application.save(racktivity_application)

    params['result']= {'returncode':True}

def match(q,i,params,tags):
    return True
