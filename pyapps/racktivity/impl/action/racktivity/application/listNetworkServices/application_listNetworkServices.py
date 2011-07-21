__author__ = 'racktivity'

__priority__ = 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    application = p.api.model.racktivity.application.get(applicationguid)

    networkservices = application.networkservices
    result = []
    for ns in networkservices:
        ips = ns.ipaddressguids or []
        rc_ports = []
        if ns.ports:
            for port in ns.ports:
                rc_ports.append({'portnr':port.portnr,'monitor':port.monitor,'ipaddress':port.ipaddress,'ipprotocoltype':str(port.ipprotocoltype)})
        result.append({'name':ns.name,'description':ns.description,'monitor':ns.monitor,'enabled':ns.enabled,'ipaddressguids':ips,'ports':rc_ports})
    params['result'] = {'returncode':True, 'networkserviceinfo':result}

def match(q,i,params,tags):
    return True

