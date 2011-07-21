__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    service = application.services.new()
    service.name = params['name']
    service.enabled = True
    if params['description']: service.description = params['description']
    application.services.append(service)
    p.api.model.racktivity.application.save(application)
    params['result'] = {'returncode':True, 'serviceguid': service.guid}

def match(q, i, params, tags):
    return True

