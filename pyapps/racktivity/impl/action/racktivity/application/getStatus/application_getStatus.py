__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    res = p.api.actor.application.getstatus(params['applicationguid'])['result']
    params['result'] =  {'returncode':True, 'status':res}

def match(q, i, params, tags):
    return True

