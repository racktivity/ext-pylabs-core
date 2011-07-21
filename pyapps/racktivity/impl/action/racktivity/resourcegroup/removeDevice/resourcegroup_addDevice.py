__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    resourcegroup = p.api.model.racktivity.resourcegroup.get(params['resourcegroupguid'])
    if params['deviceguid'] in resourcegroup.deviceguids:
        resourcegroup.deviceguids.remove(params['deviceguid'])
    p.api.model.racktivity.resourcegroup.save(resourcegroup)
    params['result'] = True

def match(q, i, params, tags):
    return True
