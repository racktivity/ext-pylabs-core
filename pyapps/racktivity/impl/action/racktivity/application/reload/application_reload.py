__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Calling actor actions to reload the application specified', 3)

    ret = p.api.actor.application.reload(applicationguid = params['applicationguid'],
                                             executionparams = {'description' : 'Reloading the application'})['result']
    params['result'] = {'returncode': ret}

def match(q, i, params, tags):
    return True
