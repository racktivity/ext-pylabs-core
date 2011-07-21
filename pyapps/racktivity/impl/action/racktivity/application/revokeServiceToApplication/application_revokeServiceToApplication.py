__author__ = 'racktivity'
__priority__= 3


def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    found = False
    for service in application.services:
        if found: break
        if service.name==params['servicename']:
            for service2 in service.service2applications:
                if service2.applicationguid==params['destinationapplicationguid']:
                    found = True
                    service.service2applications.remove(service2)
                    p.api.model.racktivity.application.save(application)
                    params['result'] = {'returncode':True}
                    break            
    if not found: raise ValueError('The service with the name or application specified could not be found!')
    
def match(q, i, params, tags):
    return True

