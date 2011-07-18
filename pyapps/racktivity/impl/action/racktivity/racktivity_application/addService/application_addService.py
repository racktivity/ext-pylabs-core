__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'addService'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    service = racktivity_application.services.new()
    service.name = params['name']
    service.enabled = True
    if params['description']: service.description = params['description']
    racktivity_application.services.append(service)
    q.drp.racktivity_application.save(racktivity_application)
    params['result'] = {'returncode':True, 'serviceguid': service.guid}

def match(q, i, params, tags):
    return True

