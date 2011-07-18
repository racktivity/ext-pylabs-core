__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'reload'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Calling actor actions to reload the racktivity_application specified', 3)

    ret = q.actions.actor.racktivity_application.reload(applicationguid = params['applicationguid'],
                                             executionparams = {'description' : 'Reloading the racktivity_application'})['result']
    params['result'] = {'returncode': ret}

def match(q, i, params, tags):
    return True
