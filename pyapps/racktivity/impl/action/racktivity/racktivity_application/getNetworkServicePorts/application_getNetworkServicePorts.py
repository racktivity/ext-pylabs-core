__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'getNetworkServicePorts'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    
    result = list()
    for ns in [networkservice for networkservice in racktivity_application.networkservices if networkservice.name == params['networkservicename']]:
        ips = ns.ipaddressguids or []
        for port in ns.ports:
            result.append({'portnr':port.portnr,'monitor':port.monitor,'ipaddress':port.ipaddress,'ipprotocoltype':str(port.ipprotocoltype)})
    params['result'] =  {'returncode':True, 'networkserviceports':result}

def match(q, i, params, tags):
    return True
