__tags__ = 'authenticate', 
__author__ = 'Incubaid'

def main(q, i, params, tags):
    request = params['request']
    criteria = params['criteria']
    domain =  params['domain']
    service = params['service']
    methodname = params['methodname']
    args = params['args']
    kwargs = params['kwargs']
    return request.username == request.password

def match(q, i, params, tags):
    return True
