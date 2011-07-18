__author__ = 'racktivity'
__tags__ = 'racktivity_application','removeNetworkServicePort'

__priority__ = 3

def main(q,i,params,tags):
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    racktivity_application = q.drp.racktivity_application.get(applicationguid)
    ns_name = params['servicename']
    p_portnr = params['portnr']

    networkservice = [svc for svc in racktivity_application.networkservices if svc.name == ns_name ]
    if not networkservice:
        q.eventhandler.raiseError('No service with name %s in racktivity_application %s' %(ns_name,applicationguid))
    networkservice = networkservice[0]

    port = [ p for p in networkservice.ports if p.portnr == p_portnr ]
    if not port:
        q.eventhandler.raiseError('No port with port %s defined on networkservice %s in racktivity_application %s' %(str(p_portnr),ns_name, applicationguid))
    port = port[0]
    networkservice.ports.remove(port)
    q.drp.racktivity_application.save(racktivity_application)
    
    params['result'] = {'returncode':True}

def match(q,i,params,tags):
    return True
