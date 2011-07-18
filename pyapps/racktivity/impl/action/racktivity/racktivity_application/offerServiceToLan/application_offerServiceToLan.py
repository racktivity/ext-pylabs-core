__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'offerServiceToLan'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    services = [service for service in racktivity_application.services if service.name == params['servicename']]
    
    if len(services) != 1:
        raise ValueError('The service name specified could not be found!')
    
    service2 = services[0].service2lans.new()
    service2.languid = params['languid']
    if params['remark']: service2.remark = params['remark']
    services[0].service2lans.append(service2)
    q.drp.racktivity_application.save(racktivity_application)
    params['result'] = {'returncode':True}
    
def match(q, i, params, tags):
    return True


