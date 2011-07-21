__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    application.status = q.enumerators.applicationstatustype.DISABLED
    p.api.model.racktivity.application.save(application)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True
