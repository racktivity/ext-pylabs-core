__author__ = 'racktivity'
__tags__ = 'ipaddress', 'setState'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    ipaddressguid = params.get('ipaddressguid',None)
    status        = params.get('status',None)
    if ipaddressguid:
         ipaddress = q.drp.ipaddress.get(ipaddressguid)
         ipaddress.status = status
         q.drp.ipaddress.save(ipaddress)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True


