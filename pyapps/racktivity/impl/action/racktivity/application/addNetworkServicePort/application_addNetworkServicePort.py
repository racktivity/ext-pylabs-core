__author__ = 'racktivity'

__priority__ = 3

def main(q, i, p, params, tags):
    """ applicationguid,servicename, portnr, protocoltype,ipaddress, monitor """
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    application = p.api.model.racktivity.application.get(applicationguid)
    ns_name = params['servicename']

    networkservice = [ svc for svc in application.networkservices if svc.name == ns_name]
    if not networkservice:
        q.eventhandler.raiseError('No networkservice with name %s for application %s' %(ns_name,applicationguid))
    networkservice = networkservice[0]
    
    port = networkservice.ports.new()
    port.portnr = params['portnr']
    port.ipprotocoltype = params['protocoltype']
    port.ipaddress = params['ipaddress']
    port.ipaddress = params['ipaddress']
    port.monitor = params['monitor']
    networkservice.ports.append(port)

    p.api.model.racktivity.application.save(application)

    params['result'] = {'returncode':True}

def match(q,i,params,tags):
    return True
