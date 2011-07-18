__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'removeService'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    
    services = [service for service in racktivity_application.services if service.name == params['servicename']]
    
    if len(services) == 0:
        q.logger.log('The service [%s] could not be found!'%params['servicename'],3)
        params['result'] = {'returncode':False}
    elif len(services) == 1:
        racktivity_application.services.remove(services[0])
        q.drp.racktivity_application.save(racktivity_application)
        params['result'] = {'returncode':True}
    else:
        raise ValueError('Multiple services found, cannot delete services')

def match(q, i, params, tags):
    return True
