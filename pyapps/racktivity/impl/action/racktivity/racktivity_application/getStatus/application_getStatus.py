__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'getStatus'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    res = q.actions.actor.racktivity_application.getstatus(params['applicationguid'])['result']
    params['result'] =  {'returncode':True, 'status':res}

def match(q, i, params, tags):
    return True

