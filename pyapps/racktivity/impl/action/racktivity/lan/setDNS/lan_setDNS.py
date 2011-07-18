__author__ = 'racktivity'
__tags__ = 'lan', 'setDNS'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    lan = q.drp.lan.get(params['languid'])
    
    for dnsip in params['dns']:
        dns = lan.dns.new()
        dns.ip = dnsip
        lan.dns.append(dns)
    jobguid = params['jobguid']
    q.drp.lan.save(lan)
   
            
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True

