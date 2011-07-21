__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    
    services = [service for service in application.services if service.name == params['servicename']]
    
    if len(services) == 0:
        q.logger.log('The service [%s] could not be found!'%params['servicename'],3)
        params['result'] = {'returncode':False}
    elif len(services) == 1:
        application.services.remove(services[0])
        p.api.model.racktivity.application.save(application)
        params['result'] = {'returncode':True}
    else:
        raise ValueError('Multiple services found, cannot delete services')

def match(q, i, params, tags):
    return True
