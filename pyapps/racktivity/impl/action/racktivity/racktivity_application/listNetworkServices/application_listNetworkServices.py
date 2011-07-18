__author__ = 'racktivity'
__tags__ = 'racktivity_application','listNetworkServices'

__priority__ = 3

def main(q,i,params,tags):
    params['result'] = {'returncode':False}
    applicationguid = params['applicationguid']
    racktivity_application = q.drp.racktivity_application.get(applicationguid)

    networkservices = racktivity_application.networkservices
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

