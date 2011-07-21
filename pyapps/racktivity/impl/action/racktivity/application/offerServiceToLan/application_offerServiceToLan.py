__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    services = [service for service in application.services if service.name == params['servicename']]
    
    if len(services) != 1:
        raise ValueError('The service name specified could not be found!')
    
    service2 = services[0].service2lans.new()
    service2.languid = params['languid']
    if params['remark']: service2.remark = params['remark']
    services[0].service2lans.append(service2)
    p.api.model.racktivity.application.save(application)
    params['result'] = {'returncode':True}
    
def match(q, i, params, tags):
    return True


