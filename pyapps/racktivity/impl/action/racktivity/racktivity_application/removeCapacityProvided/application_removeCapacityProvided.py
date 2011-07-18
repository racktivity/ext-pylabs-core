__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'removeCapacityProvided'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    racktivity_application = q.drp.racktivity_application.get(params['applicationguid'])
    cu = [cu for cu in racktivity_application.capacityunitsprovided if str(cu.capacityunittype) == params['capacityunittype']]
    
    if len(cu) != 1:
        raise ValueError('The capacity unit type specified could not be found!')
    
    racktivity_application.capacityunitsprovided.remove(cu[0])
    q.drp.racktivity_application.save(racktivity_application)
    params['result'] = {'returncode':True}

def match(q, i, params, tags):
    return True