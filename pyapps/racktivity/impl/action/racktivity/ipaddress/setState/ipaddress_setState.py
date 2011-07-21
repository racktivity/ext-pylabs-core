__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    ipaddressguid = params.get('ipaddressguid',None)
    status        = params.get('status',None)
    if ipaddressguid:
         ipaddress = p.api.model.racktivity.ipaddress.get(ipaddressguid)
         ipaddress.status = status
         p.api.model.racktivity.ipaddress.save(ipaddress)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True


