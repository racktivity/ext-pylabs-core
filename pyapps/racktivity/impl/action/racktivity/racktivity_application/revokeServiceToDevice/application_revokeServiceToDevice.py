__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'revokeServiceToDevice'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    found = False
    for service in racktivity_application.services:
        if found: break
        if service.name==params['servicename']:
            for service2 in service.service2devices:
                if service2.deviceguid==params['deviceguid']:
                    found = True
                    service.service2devices.remove(service2)
                    q.drp.racktivity_application.save(racktivity_application)
                    params['result'] = {'returncode':True}
                    break            
    if not found: raise ValueError('The service with the name or device specified could not be found!')
    
def match(q, i, params, tags):
    return True
