__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    application = p.api.model.racktivity.application.get(params['applicationguid'])
    
    cu = [cu for cu in application.capacityunitsconsumed if str(cu.capacityunittype) == params['capacityunittype']]
    
    if len(cu) != 1:
        raise ValueError('The capacity unit type specified could not be found!')
    
    application.capacityunitsconsumed.remove(cu[0])
    p.api.model.racktivity.application.save(application)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True