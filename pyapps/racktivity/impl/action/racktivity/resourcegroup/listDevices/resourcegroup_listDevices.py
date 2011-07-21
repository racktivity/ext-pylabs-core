__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    resource = p.api.model.racktivity.resourcegroup.get(params['resourcegroupguid'])
    
    params['result'] = {'returncode': True,
                        'guidlist': [guid for guid in resource.deviceguids]}

def match(q, i, params, tags):
    return True


