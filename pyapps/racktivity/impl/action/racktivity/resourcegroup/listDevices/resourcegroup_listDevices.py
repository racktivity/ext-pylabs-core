__author__ = 'aserver'
__tags__ = 'resourcegroup', 'listDevices'
__priority__= 3

def main(q, i, params, tags):
    resource = q.drp.resourcegroup.get(params['resourcegroupguid'])
    
    params['result'] = {'returncode': True,
                        'guidlist': [guid for guid in resource.deviceguids]}

def match(q, i, params, tags):
    return True


