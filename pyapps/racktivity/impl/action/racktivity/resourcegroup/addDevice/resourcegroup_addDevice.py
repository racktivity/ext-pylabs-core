__author__ = 'aserver'
__priority__= 3

def main(q, i, p, params, tags):
    resourcegroup = p.api.model.racktivity.resourcegroup.get(params['resourcegroupguid'])
    if not params['deviceguid'] in resourcegroup.deviceguids:
        resourcegroup.deviceguids.append(params['deviceguid'])
    p.api.model.racktivity.resourcegroup.save(resourcegroup)
    params['result'] = True

def match(q, i, params, tags):
    return True
