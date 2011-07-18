__author__ = 'racktivity'
__tags__ = 'racktivity_application','addNetworkServicePort'

__priority__ = 3

def main(q,i,params,tags):
    """ applicationguid,servicename, portnr, protocoltype,ipaddress, monitor """
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    racktivity_application = q.drp.racktivity_application.get(applicationguid)
    ns_name = params['servicename']

    networkservice = [ svc for svc in racktivity_application.networkservices if svc.name == ns_name]
    if not networkservice:
        q.eventhandler.raiseError('No networkservice with name %s for racktivity_application %s' %(ns_name,applicationguid))
    networkservice = networkservice[0]
    
    port = networkservice.ports.new()
    port.portnr = params['portnr']
    port.ipprotocoltype = params['protocoltype']
    port.ipaddress = params['ipaddress']
    port.ipaddress = params['ipaddress']
    port.monitor = params['monitor']
    networkservice.ports.append(port)

    q.drp.racktivity_application.save(racktivity_application)

    params['result'] = {'returncode':True}

def match(q,i,params,tags):
    return True
