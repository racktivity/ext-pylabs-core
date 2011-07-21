__author__ = 'racktivity'

__priority__ = 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    application = p.api.model.racktivity.application.get(applicationguid)
    ns_name = params['servicename']
    p_portnr = params['portnr']

    networkservice = [svc for svc in application.networkservices if svc.name == ns_name ]
    if not networkservice:
        q.eventhandler.raiseError('No service with name %s in application %s' %(ns_name,applicationguid))
    networkservice = networkservice[0]

    port = [ p for p in networkservice.ports if p.portnr == p_portnr ]
    if not port:
        q.eventhandler.raiseError('No port with port %s defined on networkservice %s in application %s' %(str(p_portnr),ns_name, applicationguid))
    port = port[0]
    networkservice.ports.remove(port)
    p.api.model.racktivity.application.save(application)
    
    params['result'] = {'returncode':True}

def match(q,i,params,tags):
    return True
