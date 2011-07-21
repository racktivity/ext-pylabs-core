__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    
    result = list()
    for ns in [networkservice for networkservice in application.networkservices if networkservice.name == params['networkservicename']]:
        ips = ns.ipaddressguids or []
        for port in ns.ports:
            result.append({'portnr':port.portnr,'monitor':port.monitor,'ipaddress':port.ipaddress,'ipprotocoltype':str(port.ipprotocoltype)})
    params['result'] =  {'returncode':True, 'networkserviceports':result}

def match(q, i, params, tags):
    return True
