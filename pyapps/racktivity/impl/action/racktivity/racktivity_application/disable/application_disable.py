__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'disable'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    racktivity_application.status = q.enumerators.applicationstatustype.DISABLED
    q.drp.racktivity_application.save(racktivity_application)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
